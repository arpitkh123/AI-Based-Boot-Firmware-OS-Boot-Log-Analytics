import { motion } from "framer-motion";

/**
 * PageTransition
 *
 * Wraps a page's root element in a Framer Motion fade animation.
 * Kept intentionally subtle (opacity only, 200ms) — appropriate for
 * engineering dashboards where quick, clean transitions are preferred
 * over dramatic visual effects.
 *
 * Usage:
 *   <PageTransition>
 *     <div>...page content...</div>
 *   </PageTransition>
 */
function PageTransition({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.18, ease: "easeInOut" }}
    >
      {children}
    </motion.div>
  );
}

export default PageTransition;
