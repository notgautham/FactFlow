import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDownIcon } from "@radix-ui/react-icons";

const FancyAccordion = ({ title, children, isOpen, onClick }) => {
  return (
    <div className="mb-2 rounded-xl overflow-hidden shadow-sm bg-background transition-all">
      <button
        onClick={onClick}
        className="flex items-center justify-between w-full px-4 py-3 font-medium text-left text-base hover:bg-muted/50 transition-colors duration-300"
      >
        <span className="hover:text-violet-500 transition-colors duration-300">{title}</span>
        <motion.div
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.3 }}
        >
          <ChevronDownIcon className="w-5 h-5 text-muted-foreground" />
        </motion.div>
      </button>

      <AnimatePresence initial={false}>
        {isOpen && (
          <motion.div
            key="content"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.4 }}
            className="px-4 pb-4 text-sm text-muted-foreground"
          >
            {children}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default FancyAccordion;
