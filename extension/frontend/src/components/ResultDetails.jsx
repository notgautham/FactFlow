import React, { useState } from "react";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Card, CardContent } from "@/components/ui/card";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { InfoCircledIcon } from "@radix-ui/react-icons";
import { motion, AnimatePresence } from "framer-motion";

const ResultDetails = ({ resultData }) => {
  if (!resultData) return null;

  const { pattern_verification, source_credibility, cross_reference } =
    resultData.details || {};

  const getColorByLabel = (label) => {
    if (!label) return "text-foreground";
    if (label.toLowerCase().includes("real")) return "text-green-500";
    if (label.toLowerCase().includes("fake")) return "text-red-500";
    if (label.toLowerCase().includes("soft")) return "text-yellow-500";
    return "text-muted-foreground";
  };

  const [openItem, setOpenItem] = useState(null);

  const handleToggle = (value) => {
    setOpenItem(openItem === value ? null : value);
  };

  return (
    <TooltipProvider>
      <motion.div
        className="space-y-4 mt-4 w-full"
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
      >
        <Accordion
          type="single"
          collapsible
          value={openItem}
          onValueChange={handleToggle}
          className="w-full space-y-2"
        >
          {/* Pattern Detection */}
          <AccordionItem value="pattern">
            <AccordionTrigger
              className={`no-underline hover:text-violet-500 text-md font-semibold px-4 py-3 rounded-lg transition-all duration-300 
              bg-background/50 backdrop-blur border border-transparent hover:border-violet-400`}
            >
              🧠 Pattern Detection (Stylistic Analysis)
              <Tooltip>
                <TooltipTrigger asChild>
                  <InfoCircledIcon className="ml-2 h-4 w-4 text-muted-foreground" />
                </TooltipTrigger>
                <TooltipContent>
                  Analyzes writing style, formatting, and language patterns typical of fake news.
                </TooltipContent>
              </Tooltip>
            </AccordionTrigger>
            <AccordionContent>
              <Card className="bg-transparent border-none shadow-none">
                <CardContent className="pt-4 text-sm space-y-2">
                  <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                    <strong>Label:</strong>{" "}
                    <span className={getColorByLabel(pattern_verification?.label)}>
                      {pattern_verification?.label || "N/A"}
                    </span>
                  </motion.p>
                  <p>
                    <strong>Confidence:</strong>{" "}
                    {(pattern_verification?.confidence * 100 || 0).toFixed(2)}%
                  </p>
                  <p>
                    <strong>Reason:</strong>{" "}
                    {pattern_verification?.reason || "N/A"}
                  </p>
                </CardContent>
              </Card>
            </AccordionContent>
          </AccordionItem>

          {/* Source Credibility */}
          <AccordionItem value="source">
            <AccordionTrigger
              className={`no-underline hover:text-violet-500 text-md font-semibold px-4 py-3 rounded-lg transition-all duration-300 
              bg-background/50 backdrop-blur border border-transparent hover:border-violet-400`}
            >
              🌐 Source Credibility (Domain Trust)
              <Tooltip>
                <TooltipTrigger asChild>
                  <InfoCircledIcon className="ml-2 h-4 w-4 text-muted-foreground" />
                </TooltipTrigger>
                <TooltipContent>
                  Uses source databases like MBFC to verify domain reliability.
                </TooltipContent>
              </Tooltip>
            </AccordionTrigger>
            <AccordionContent>
              <Card className="bg-transparent border-none shadow-none">
                <CardContent className="pt-4 text-sm space-y-2">
                  <p><strong>Domain:</strong> {source_credibility?.domain || "N/A"}</p>
                  <p><strong>Credibility Rating:</strong> {source_credibility?.credibility_rating || "N/A"}</p>
                  <p><strong>Bias:</strong> {source_credibility?.bias || "N/A"}</p>
                  <p><strong>MBFC Score:</strong> {source_credibility?.score || "N/A"}</p>
                  <p><strong>Note:</strong> {source_credibility?.note || "N/A"}</p>
                  <p className="text-xs italic text-muted-foreground">
                    {source_credibility?.reason || ""}
                  </p>
                </CardContent>
              </Card>
            </AccordionContent>
          </AccordionItem>

          {/* Cross Reference */}
          <AccordionItem value="crossref">
            <AccordionTrigger
              className={`no-underline hover:text-violet-500 text-md font-semibold px-4 py-3 rounded-lg transition-all duration-300 
              bg-background/50 backdrop-blur border border-transparent hover:border-violet-400`}
            >
              📚 Cross-Reference (Factual Verification)
              <Tooltip>
                <TooltipTrigger asChild>
                  <InfoCircledIcon className="ml-2 h-4 w-4 text-muted-foreground" />
                </TooltipTrigger>
                <TooltipContent>
                  Verifies claims against reliable fact databases.
                </TooltipContent>
              </Tooltip>
            </AccordionTrigger>
            <AccordionContent>
              <Card className="bg-transparent border-none shadow-none">
                <CardContent className="pt-4 text-sm space-y-2">
                  <p>
                    <strong>Verdict:</strong>{" "}
                    <span className={getColorByLabel(cross_reference?.verdict)}>
                      {cross_reference?.verdict || "N/A"}
                    </span>
                  </p>
                  <p><strong>Summary:</strong> {cross_reference?.summary || "N/A"}</p>
                  {cross_reference?.issues?.length > 0 && (
                    <div className="mt-2 space-y-2">
                      <h4 className="font-semibold">⚠️ Flagged Claims:</h4>
                      {cross_reference.issues.map((issue, idx) => (
                        <motion.div
                          key={idx}
                          className="p-3 rounded-md bg-muted/10"
                          initial={{ opacity: 0, y: 5 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: 0.1 * idx }}
                        >
                          <p><strong>Claim:</strong> {issue.claim}</p>
                          <p className="text-muted-foreground">
                            <strong>Explanation:</strong> {issue.explanation}
                          </p>
                        </motion.div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            </AccordionContent>
          </AccordionItem>
        </Accordion>
      </motion.div>
    </TooltipProvider>
  );
};

export default ResultDetails;
