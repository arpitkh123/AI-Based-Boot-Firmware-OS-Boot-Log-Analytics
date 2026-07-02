from src.config.fusion_config import FusionConfig

class ConfidenceFusion:
    """
    Implements a hybrid confidence scoring algorithm combining Rule Engine matches,
    Knowledge Base matches, Isolation Forest anomalies, Boot Health, and Severity.
    """
    def __init__(self, config: FusionConfig = None):
        self.config = config if config else FusionConfig()
        self.weights = self.config.get_weights()
        
    def calculate_confidence(self, rule_anomalies: list, ml_anomaly: dict, boot_analysis: dict, template_stats: dict) -> dict:
        """
        Calculates the final confidence score and returns a fusion result.
        The returned dictionary matches the structure expected by the backend analyzer.
        """
        # Calculate individual normalized scores (0 to 1)
        
        # 1. Rule / KB Match
        s_rule = 0.0
        s_kb = 0.0
        s_severity = 0.0
        
        if rule_anomalies:
            s_rule = 1.0
            # Check if any rule came from the KB
            kb_matches = [a for a in rule_anomalies if a.get("model") == "KNOWLEDGE_BASE"]
            if kb_matches:
                # Use the highest confidence from KB
                conf_map = {"HIGH": 1.0, "MEDIUM": 0.7, "LOW": 0.4}
                max_kb_conf = max([conf_map.get(a.get("kb_confidence", "MEDIUM"), 0.7) for a in kb_matches])
                s_kb = max_kb_conf
                
            # Use max severity from rules
            if any(a.get("severity") == "CRITICAL" for a in rule_anomalies):
                s_severity = 1.0
            elif any(a.get("severity") == "WARNING" for a in rule_anomalies):
                s_severity = 0.5
        
        # 2. ML Anomaly Strength (0 to 1)
        s_if = ml_anomaly.get("anomaly_strength", 0.0) / 100.0
        
        # 3. Template Similarity (inverse of new templates ratio)
        total_templates = template_stats.get("total_templates", 1)
        # Using a fallback if new_templates is missing
        new_templates = template_stats.get("new_templates", 0) 
        s_ts = 1.0 - (new_templates / max(total_templates, 1))
        
        # 4. Boot Health
        s_bh = 1.0 if not boot_analysis.get("boot_successful", True) else 0.0
        if not s_bh and s_severity == 0:
            # If boot was successful and no rules hit, severity from ML is used
            s_severity = s_if
            
        # If there's an ML prediction but no rule, the ML severity dominates
        if not rule_anomalies and ml_anomaly.get("prediction") != "NORMAL":
            if s_if > 0.8:
                s_severity = 1.0
            elif s_if > 0.4:
                s_severity = 0.5
                
        # Calculate weighted sum
        W = self.weights
        numerator = (
            W["rule_match"] * s_rule +
            W["kb_match"] * s_kb +
            W["iforest_score"] * s_if +
            W["template_sim"] * s_ts +
            W["boot_health"] * s_bh +
            W["severity"] * s_severity
        )
        denominator = sum(W.values())
        
        final_confidence = numerator / denominator if denominator > 0 else 0.0
        
        # Map to class and severity for the API output
        if rule_anomalies:
            pred_class = "KNOWN_FAILURE"
        else:
            pred_class = ml_anomaly.get("prediction", "NORMAL")
            
        final_confidence_percentage = round(final_confidence * 100, 2)
        
        return {
            "prediction": pred_class,
            "anomaly_strength": final_confidence_percentage,
            "anomaly_score": final_confidence,
            "rule_matches": rule_anomalies,
            "ml_original": ml_anomaly
        }
