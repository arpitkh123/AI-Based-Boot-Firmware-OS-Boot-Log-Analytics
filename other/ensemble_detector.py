import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import re
import os
import json
import joblib
from groq import Groq
from drain3 import TemplateMiner
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer

class LSTMAutoencoder(nn.Module):
    def __init__(self, num_templates, embedding_dim=16, hidden_dim=32, seq_len=10):
        super(LSTMAutoencoder, self).__init__()
        self.seq_len = seq_len
        self.hidden_dim = hidden_dim
        # Padding index allows us to safely handle unseen templates in new logs
        self.embedding = nn.Embedding(num_embeddings=num_templates + 50, embedding_dim=embedding_dim)
        self.encoder_lstm = nn.LSTM(input_size=embedding_dim + 1, hidden_size=hidden_dim, batch_first=True)
        self.decoder_lstm = nn.LSTM(input_size=hidden_dim, hidden_size=hidden_dim, batch_first=True)
        self.out_template = nn.Linear(hidden_dim, num_templates + 50)
        self.out_delta = nn.Linear(hidden_dim, 1)
        
    def forward(self, x):
        template_ids = x[:, :, 0].long()
        delta_t = x[:, :, 1].unsqueeze(-1).float()
        emb = self.embedding(template_ids)
        lstm_in = torch.cat((emb, delta_t), dim=2)
        _, (hidden, _) = self.encoder_lstm(lstm_in)
        hidden = hidden.transpose(0, 1).repeat(1, self.seq_len, 1)
        decoder_out, _ = self.decoder_lstm(hidden)
        pred_template = self.out_template(decoder_out)
        pred_delta = self.out_delta(decoder_out)
        return pred_template, pred_delta

class EnsembleDetector:
    def __init__(self, seq_len=10):
        self.seq_len = seq_len
        self.miner = TemplateMiner()
        self.iforest = IsolationForest(contamination=0.05, random_state=42)
        self.vectorizer = TfidfVectorizer(max_features=50, stop_words='english')
        # U-Boot dedicated IForest (text-only, no timestamps)
        self.uboot_iforest = IsolationForest(contamination=0.10, random_state=42)
        self.uboot_vectorizer = TfidfVectorizer(max_features=30, stop_words='english')
        self.uboot_iforest_trained = False
        self.lstm_model = None
        self.lstm_threshold = 0
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.is_trained = False
        self.num_templates = 0
        
        # Initialize Groq for Root Cause Analysis
        self.groq_client = None
        if os.environ.get("GROQ_API_KEY"):
            try:
                self.groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            except Exception as e:
                print(f"Warning: Failed to initialize Groq client: {e}")
        
        # Load offline knowledge base
        self.knowledge_base = []
        kb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'knowledge_base.json')
        if os.path.exists(kb_path):
            try:
                with open(kb_path, 'r', encoding='utf-8') as f:
                    self.knowledge_base = json.load(f).get('patterns', [])
            except Exception as e:
                print(f"Warning: Failed to load knowledge base: {e}")
                
    def lookup_knowledge_base(self, text):
        """Check the offline knowledge base for a matching resolution."""
        text_lower = text.lower()
        for entry in self.knowledge_base:
            if re.search(entry['match'], text_lower):
                return {
                    'type': entry['type'],
                    'resolution': entry['resolution'],
                    'confidence': entry['confidence'],
                    'source': 'KNOWLEDGE_BASE'
                }
        return None

    def analyze_root_cause(self, anomaly, context_lines=None, boot_phase='kernel', bootargs=None):
        """Context-aware root cause analysis. Checks KB first, falls back to Groq."""
        payload = anomaly.get('reason', '')
        raw = anomaly.get('raw', '')
        
        # Step 1: Check knowledge base against multiple text sources (instant, offline)
        search_texts = [payload, raw]
        if context_lines:
            search_texts.append(context_lines.get('anomaly', ''))
            search_texts.extend(context_lines.get('before', [])[-3:])
        
        kb_result = None
        for text in search_texts:
            if text:
                kb_result = self.lookup_knowledge_base(text)
                if kb_result:
                    break
        
        if kb_result:
            return f"Type: {kb_result['type']}\nResolution: {kb_result['resolution']}\nSource: Knowledge Base ({kb_result['confidence']} confidence)"
        
        # Step 2: Fall back to Groq with full context
        if not self.groq_client:
            return "No knowledge base match found. Set GROQ_API_KEY for AI-powered resolution."
        
        # Build context-rich prompt
        context_block = ""
        if context_lines:
            before = context_lines.get('before', [])
            after = context_lines.get('after', [])
            if before:
                context_block += "PRECEDING CONTEXT (lines before the anomaly):\n"
                for line in before[-10:]:
                    context_block += f"  {line}\n"
            context_block += f"\nANOMALY LINE:\n  {anomaly.get('raw', payload)}\n"
            if after:
                context_block += f"\nFOLLOWING CONTEXT (lines after the anomaly):\n"
                for line in after[:5]:
                    context_block += f"  {line}\n"
        else:
            context_block = f"ANOMALY: {payload}"
        
        meta = f"BOOT PHASE: {boot_phase}\n"
        meta += f"SEVERITY: {anomaly.get('severity', 'UNKNOWN')}\n"
        meta += f"DETECTION MODEL: {anomaly.get('model', 'UNKNOWN')}\n"
        if bootargs:
            meta += f"BOOT ARGUMENTS: {bootargs}\n"
        
        full_prompt = f"{meta}\n{context_block}"
        
        try:
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": """You are a Linux Kernel and Embedded Systems expert diagnosing Raspberry Pi boot logs.
The user provides an anomalous log line with surrounding context, boot phase, and metadata.
Analyze the full context to determine the root cause.

Reply with exactly three lines:
Line 1: 'Type: <Short Error Type>'
Line 2: 'Resolution: <Specific, actionable fix with exact commands or config changes>'
Line 3: 'Source: AI Analysis (Groq)'

Be specific. Reference exact config files, commands, and parameters."""
                    },
                    {
                        "role": "user",
                        "content": full_prompt
                    }
                ],
                model="llama-3.3-70b-versatile",
                max_tokens=250,
                temperature=0.2
            )
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            return f"Type: API Error\nResolution: {e}"
        
    def preprocess(self, filepath):
        with open(filepath, 'r', errors='ignore') as f:
            lines = f.readlines()
            
        kernel_pattern = re.compile(r'^\[\s*([\d\.]+)\]\s+(.*)')
        parsed_logs = []
        uboot_lines = []  # Store raw U-Boot lines for analysis
        uboot_backspaces = 0
        
        # If the file doesn't look like a full boot (e.g., just a dmesg snippet from github), skip u-boot
        phase = 'uboot'
        if not any('Starting kernel' in l for l in lines[:200]):
            phase = 'kernel'
            
        for idx, line in enumerate(lines):
            line = line.strip('\n')
            if 'Starting kernel ...' in line:
                phase = 'kernel'
                continue
                
            if phase == 'uboot':
                uboot_backspaces += line.count('\b')
                uboot_lines.append({'line_no': idx + 1, 'text': line})
            else:
                match = kernel_pattern.search(line)
                if match:
                    timestamp = float(match.group(1))
                    payload = match.group(2)
                    
                    result = self.miner.add_log_message(payload)
                    template_id = result["cluster_id"]
                    
                    parsed_logs.append({
                        'line_no': idx + 1,
                        'timestamp': timestamp,
                        'template_id': template_id,
                        'payload': payload,
                        'raw': line
                    })
                elif "panic" in line.lower() or "error" in line.lower() or "fail" in line.lower() or "bug" in line.lower():
                     # Catch raw kernel panics or crash dumps that lack standard timestamps
                     parsed_logs.append({
                        'line_no': idx + 1,
                        'timestamp': None,
                        'template_id': 0, # Unknown/out-of-band template
                        'payload': line,
                        'raw': line
                    })

        df = pd.DataFrame(parsed_logs)
        if not df.empty:
            df['timestamp'] = df['timestamp'].ffill().fillna(0)
            df['delta_t'] = df['timestamp'].diff().fillna(0)
            df['delta_t_scaled'] = np.log1p(df['delta_t'].clip(lower=0))
        return df, uboot_backspaces, uboot_lines

    def extract_iforest_features(self, df, is_training=False):
        if df.empty:
            return df
        
        keywords = ['error', 'fail', 'unable', 'invalid', 'panic']
        for kw in keywords:
             df[f'kw_{kw}'] = df['payload'].str.lower().str.contains(kw).astype(int)
                
        if is_training:
            tfidf_features = self.vectorizer.fit_transform(df['payload'].fillna('')).toarray()
        else:
            tfidf_features = self.vectorizer.transform(df['payload'].fillna('')).toarray()
            
        for i in range(tfidf_features.shape[1]):
            df[f'tfidf_{i}'] = tfidf_features[:, i]
        return df
        
    def extract_lstm_sequences(self, df):
        sequences = []
        indices = []
        if len(df) < self.seq_len:
            return np.array([]), []
            
        for i in range(len(df) - self.seq_len + 1):
            window = df.iloc[i:i+self.seq_len]
            seq = window[['template_id', 'delta_t_scaled']].values
            sequences.append(seq)
            indices.append(window.index[-1])
        return np.array(sequences), indices

    def apply_uboot_rules(self, uboot_lines, uboot_backspaces):
        """Model A-1: Dedicated U-Boot Phase Rule Engine."""
        anomalies = []
        
        if uboot_backspaces > 10:
            anomalies.append({"line": "U-Boot Phase", "reason": f"High manual intervention ({uboot_backspaces} backspaces)", "severity": "WARNING", "model": "RULE_UBOOT"})
        
        bootp_count = 0
        card_fail_count = 0
        card_fail_text = ""
        
        for entry in uboot_lines:
            line_no = entry['line_no']
            text = entry['text']
            text_lower = text.lower()
            
            # SD Card hardware failure
            if 'card did not respond to voltage select' in text_lower:
                card_fail_count += 1
                card_fail_text = text
            
            # EFI / Boot manager failures
            if 'boot failed' in text_lower:
                anomalies.append({"line": line_no, "reason": f"Boot Manager Failure: {text.strip()[:80]}", "severity": "CRITICAL", "model": "RULE_UBOOT", "raw": text})
            if 'cannot load any image' in text_lower:
                anomalies.append({"line": line_no, "reason": "No bootable image found", "severity": "CRITICAL", "model": "RULE_UBOOT", "raw": text})
                
            # Network PHY timeout
            if 'phy_startup failed' in text_lower or ('timeout' in text_lower and 'phy' in text_lower):
                anomalies.append({"line": line_no, "reason": "Network PHY startup failure / timeout", "severity": "WARNING", "model": "RULE_UBOOT", "raw": text})
            
            # Missing boot environment
            if 'unable to read' in text_lower and 'uboot.env' in text_lower:
                anomalies.append({"line": line_no, "reason": "Missing U-Boot environment file (uboot.env)", "severity": "WARNING", "model": "RULE_UBOOT", "raw": text})
                
            # Missing bootargs
            if '"bootargs" not defined' in text_lower or 'bootargs not defined' in text_lower:
                anomalies.append({"line": line_no, "reason": "Kernel boot arguments (bootargs) not defined", "severity": "CRITICAL", "model": "RULE_UBOOT", "raw": text})
            
            # Device tree / FDT failures
            if 'fdt and atags support not compiled in' in text_lower:
                anomalies.append({"line": line_no, "reason": "Missing Device Tree (FDT) support — boot will fail", "severity": "CRITICAL", "model": "RULE_UBOOT", "raw": text})
            
            # System reset
            if text.strip() == 'resetting ...':
                anomalies.append({"line": line_no, "reason": "System reset triggered (crash or watchdog)", "severity": "CRITICAL", "model": "RULE_UBOOT", "raw": text})
            
            # BOOTP retry loop detection
            if 'bootp broadcast' in text_lower:
                bootp_count += 1
            if 'retry time exceeded' in text_lower:
                anomalies.append({"line": line_no, "reason": f"Network boot retry loop exhausted ({bootp_count} BOOTP broadcasts)", "severity": "WARNING", "model": "RULE_UBOOT", "raw": text})
                bootp_count = 0  # Reset for next retry cycle
        
        # Aggregate SD card failures (report once, not per-line)
        if card_fail_count > 0:
            anomalies.append({"line": "U-Boot Phase", "reason": f"SD Card not responding ({card_fail_count}x voltage select failures)", "severity": "CRITICAL", "model": "RULE_UBOOT", "raw": card_fail_text})
        
        return anomalies

    def apply_uboot_iforest(self, uboot_lines):
        """Model A-3: U-Boot Isolation Forest for catching novel/unknown errors."""
        anomalies = []
        if not self.uboot_iforest_trained or len(uboot_lines) < 3:
            return anomalies
        
        texts = [entry['text'] for entry in uboot_lines if entry['text'].strip()]
        if len(texts) < 3:
            return anomalies
        
        try:
            tfidf = self.uboot_vectorizer.transform(texts).toarray()
            preds = self.uboot_iforest.predict(tfidf)
            scores = self.uboot_iforest.decision_function(tfidf)
            
            for i, (pred, score) in enumerate(zip(preds, scores)):
                if pred == -1:
                    text = texts[i].strip()
                    line_no = uboot_lines[i]['line_no']
                    # Only flag if it wasn't already caught by rules
                    # and the text looks meaningful (not just whitespace/noise)
                    if len(text) > 10 and score < -0.15:
                        anomalies.append({
                            "line": line_no,
                            "reason": f"U-Boot Statistical Outlier -> {text[:70]}",
                            "severity": "WARNING",
                            "model": "IFOREST_UBOOT",
                            "raw": text
                        })
        except Exception:
            pass  # Gracefully skip if vectorizer sees unseen vocabulary
        
        return anomalies

    def apply_kernel_rules(self, df):
        """Model A-2: Kernel Phase Rule Engine."""
        anomalies = []
             
        for _, row in df.iterrows():
            msg = str(row['payload']).lower()
            raw = str(row.get('raw', row['payload']))
            if 'unknown kernel command line parameters' in msg:
                anomalies.append({"line": row['line_no'], "reason": "Broken bootargs", "severity": "CRITICAL", "model": "RULE_KERNEL", "raw": raw})
            if 'unable to register' in msg and 'port' in msg:
                anomalies.append({"line": row['line_no'], "reason": "UART Registration Failure", "severity": "CRITICAL", "model": "RULE_KERNEL", "raw": raw})
            if 'kernel panic' in msg or 'end kernel panic' in msg or 'kernel bug' in msg:
                anomalies.append({"line": row['line_no'], "reason": "Kernel Panic / Crash", "severity": "CRITICAL", "model": "RULE_KERNEL", "raw": raw})
            if 'oops' in msg and ('bug' in msg or 'error' in msg):
                anomalies.append({"line": row['line_no'], "reason": "Kernel Oops", "severity": "CRITICAL", "model": "RULE_KERNEL", "raw": raw})
            if 'out of memory' in msg and 'kill process' in msg:
                anomalies.append({"line": row['line_no'], "reason": "OOM Killer activated", "severity": "CRITICAL", "model": "RULE_KERNEL", "raw": raw})
            if 'null pointer dereference' in msg:
                anomalies.append({"line": row['line_no'], "reason": "NULL Pointer Dereference", "severity": "CRITICAL", "model": "RULE_KERNEL", "raw": raw})
            if 'segfault' in msg:
                anomalies.append({"line": row['line_no'], "reason": "Segmentation Fault", "severity": "CRITICAL", "model": "RULE_KERNEL", "raw": raw})
            if 'i/o error' in msg or 'io error' in msg:
                anomalies.append({"line": row['line_no'], "reason": f"I/O Error: {row['payload'][:60]}", "severity": "WARNING", "model": "RULE_KERNEL", "raw": raw})
            if 'timeout waiting for hardware' in msg:
                anomalies.append({"line": row['line_no'], "reason": "Hardware timeout (possible SD card issue)", "severity": "WARNING", "model": "RULE_KERNEL", "raw": raw})
            if row.get('delta_t', 0) > 1.5:
                anomalies.append({"line": row['line_no'], "reason": f"Large timing gap ({row['delta_t']:.2f}s)", "severity": "WARNING", "model": "RULE_KERNEL", "raw": raw})
        return anomalies

    def train(self, filepath):
        print(f"Training ensemble on {filepath}...")
        df, uboot_backs, uboot_lines = self.preprocess(filepath)
        if df.empty:
            raise ValueError("Training file contains no kernel logs.")
            
        self.num_templates = len(self.miner.drain.clusters)
        
        # 1. Train Kernel Isolation Forest
        df_if = self.extract_iforest_features(df.copy(), is_training=True)
        if_features = ['delta_t'] + [col for col in df_if.columns if col.startswith('kw_') or col.startswith('tfidf_')]
        self.iforest.fit(df_if[if_features].fillna(0))
        
        # 2. Train U-Boot Isolation Forest (text-only, no timestamps)
        uboot_texts = [e['text'] for e in uboot_lines if e['text'].strip() and len(e['text'].strip()) > 5]
        if len(uboot_texts) >= 5:
            uboot_tfidf = self.uboot_vectorizer.fit_transform(uboot_texts).toarray()
            self.uboot_iforest.fit(uboot_tfidf)
            self.uboot_iforest_trained = True
            print(f"  U-Boot IForest trained on {len(uboot_texts)} lines")
        
        # 3. Train LSTM
        X, _ = self.extract_lstm_sequences(df)
        self.lstm_model = LSTMAutoencoder(num_templates=self.num_templates, seq_len=self.seq_len).to(self.device)
        
        criterion_t = nn.CrossEntropyLoss()
        criterion_d = nn.MSELoss()
        optimizer = torch.optim.Adam(self.lstm_model.parameters(), lr=0.01)
        
        X_tensor = torch.tensor(X, dtype=torch.float32).to(self.device)
        
        self.lstm_model.train()
        for epoch in range(40):
            optimizer.zero_grad()
            pred_t, pred_d = self.lstm_model(X_tensor)
            
            target_t = X_tensor[:, :, 0].long()
            target_d = X_tensor[:, :, 1].unsqueeze(-1)
            
            loss = criterion_t(pred_t.transpose(1, 2), target_t) + criterion_d(pred_d, target_d)
            loss.backward()
            optimizer.step()
            
        # Set LSTM Anomaly Threshold
        self.lstm_model.eval()
        with torch.no_grad():
            pred_t, pred_d = self.lstm_model(X_tensor)
            errors = []
            for i in range(len(X_tensor)):
                t_err = criterion_t(pred_t[i].unsqueeze(0).transpose(1, 2), target_t[i].unsqueeze(0)).item()
                d_err = criterion_d(pred_d[i], target_d[i].unsqueeze(0)).item()
                errors.append(t_err + d_err)
        
        self.lstm_threshold = np.mean(errors) + 2 * np.std(errors)
        self.is_trained = True
        print(f"Training complete. LSTM threshold set to: {self.lstm_threshold:.4f}")

    def save_models(self, model_dir='models'):
        """Persist all trained models to disk for instant loading."""
        import jsonpickle
        os.makedirs(model_dir, exist_ok=True)
        
        # 1. Save LSTM weights
        torch.save(self.lstm_model.state_dict(), os.path.join(model_dir, 'lstm_weights.pt'))
        
        # 2. Save Isolation Forest (Kernel)
        joblib.dump(self.iforest, os.path.join(model_dir, 'iforest.pkl'))
        
        # 3. Save TF-IDF Vectorizer (Kernel)
        joblib.dump(self.vectorizer, os.path.join(model_dir, 'tfidf_vectorizer.pkl'))
        
        # 3b. Save U-Boot IForest + Vectorizer
        if self.uboot_iforest_trained:
            joblib.dump(self.uboot_iforest, os.path.join(model_dir, 'uboot_iforest.pkl'))
            joblib.dump(self.uboot_vectorizer, os.path.join(model_dir, 'uboot_tfidf.pkl'))
        
        # 4. Save Drain3 state via jsonpickle
        state = jsonpickle.encode(self.miner.drain)
        with open(os.path.join(model_dir, 'drain3_state.json'), 'w') as f:
            f.write(state)
        
        # 5. Save metadata (thresholds, config)
        meta = {
            'lstm_threshold': self.lstm_threshold,
            'num_templates': self.num_templates,
            'seq_len': self.seq_len,
        }
        with open(os.path.join(model_dir, 'metadata.json'), 'w') as f:
            json.dump(meta, f, indent=2)
        
        print(f"Models saved to {model_dir}/")

    def load_models(self, model_dir='models'):
        """Load previously saved models for instant inference."""
        import jsonpickle
        meta_path = os.path.join(model_dir, 'metadata.json')
        if not os.path.exists(meta_path):
            return False
        
        try:
            # 1. Load metadata
            with open(meta_path, 'r') as f:
                meta = json.load(f)
            self.lstm_threshold = meta['lstm_threshold']
            self.num_templates = meta['num_templates']
            self.seq_len = meta['seq_len']
            
            # 2. Load LSTM
            self.lstm_model = LSTMAutoencoder(
                num_templates=self.num_templates, seq_len=self.seq_len
            ).to(self.device)
            self.lstm_model.load_state_dict(
                torch.load(os.path.join(model_dir, 'lstm_weights.pt'), map_location=self.device)
            )
            self.lstm_model.eval()
            
            # 3. Load Isolation Forest
            self.iforest = joblib.load(os.path.join(model_dir, 'iforest.pkl'))
            
            # 4. Load TF-IDF (Kernel)
            self.vectorizer = joblib.load(os.path.join(model_dir, 'tfidf_vectorizer.pkl'))
            
            # 4b. Load U-Boot IForest + Vectorizer
            uboot_if_path = os.path.join(model_dir, 'uboot_iforest.pkl')
            if os.path.exists(uboot_if_path):
                self.uboot_iforest = joblib.load(uboot_if_path)
                self.uboot_vectorizer = joblib.load(os.path.join(model_dir, 'uboot_tfidf.pkl'))
                self.uboot_iforest_trained = True
            
            # 5. Load Drain3 state via jsonpickle
            drain_path = os.path.join(model_dir, 'drain3_state.json')
            if os.path.exists(drain_path):
                with open(drain_path, 'r') as f:
                    state = f.read()
                self.miner.drain = jsonpickle.decode(state)
            
            self.is_trained = True
            print(f"Models loaded from {model_dir}/ (threshold={self.lstm_threshold:.4f})")
            return True
        except Exception as e:
            print(f"Warning: Failed to load models: {e}")
            return False

    def detect(self, filepath):
        if not self.is_trained:
            raise RuntimeError("Model must be trained before calling detect()")
            
        df, uboot_backs, uboot_lines = self.preprocess(filepath)
        
        # Aggregate anomalies from all models
        report = self.apply_uboot_rules(uboot_lines, uboot_backs)
        # U-Boot IForest: catch novel errors the Rule Engine doesn't know about
        uboot_if_anomalies = self.apply_uboot_iforest(uboot_lines)
        # Only keep U-Boot IForest anomalies that weren't already caught by rules
        rule_lines = {a['line'] for a in report}
        for a in uboot_if_anomalies:
            if a['line'] not in rule_lines:
                report.append(a)
        if not df.empty:
            report += self.apply_kernel_rules(df)
        
        if df.empty:
            return report
            
        # Model B: Isolation Forest
        df_if = self.extract_iforest_features(df.copy(), is_training=False)
        if_features = ['delta_t'] + [col for col in df_if.columns if col.startswith('kw_') or col.startswith('tfidf_')]
        for col in if_features:
            if col not in df_if.columns:
                df_if[col] = 0
                
        iforest_preds = self.iforest.predict(df_if[if_features].fillna(0))
        for idx, pred in enumerate(iforest_preds):
            if pred == -1:
                line_no = df.iloc[idx]['line_no']
                payload = df.iloc[idx]['payload']
                # Suppress minor statistical noise unless it involves errors or high deltas
                if df.iloc[idx]['delta_t'] > 0.5 or any(k in payload.lower() for k in ['error', 'fail', 'panic', 'bug']):
                     report.append({"line": line_no, "reason": f"Statistical Outlier -> {payload[:60]}...", "severity": "WARNING", "model": "IFOREST"})
                
        # Model C: PyTorch LSTM
        X, indices = self.extract_lstm_sequences(df)
        if len(X) > 0:
            X_tensor = torch.tensor(X, dtype=torch.float32).to(self.device)
            # Clamp unseen template IDs to avoid embedding lookup errors
            X_tensor[:,:,0] = torch.clamp(X_tensor[:,:,0], max=self.num_templates+49) 
            
            self.lstm_model.eval()
            with torch.no_grad():
                pred_t, pred_d = self.lstm_model(X_tensor)
                criterion_t = nn.CrossEntropyLoss()
                criterion_d = nn.MSELoss()
                
                target_t = X_tensor[:, :, 0].long()
                target_d = X_tensor[:, :, 1].unsqueeze(-1)
                
                for i in range(len(X_tensor)):
                    t_err = criterion_t(pred_t[i].unsqueeze(0).transpose(1, 2), target_t[i].unsqueeze(0)).item()
                    d_err = criterion_d(pred_d[i], target_d[i].unsqueeze(0)).item()
                    err = t_err + d_err
                    if err > self.lstm_threshold:
                        line_no = df.iloc[indices[i]]['line_no']
                        # Check if already flagged by Rule to avoid double reporting
                        if not any(a['line'] == line_no for a in report):
                            report.append({"line": line_no, "reason": f"Sequence Deviation (Score {err:.2f})", "severity": "WARNING", "model": "LSTM"})
                        
        # Sort report by line number
        def sort_key(x):
            try: return int(x['line'])
            except: return 0
        report.sort(key=sort_key)
        
        return report
