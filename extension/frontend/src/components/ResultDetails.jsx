import React from "react";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Card, CardContent } from "@/components/ui/card";

const ResultDetails = ({ resultData }) => {
  if (!resultData) return null;

  const { pattern_verification, source_credibility, cross_reference } = resultData.details || {};

  return (
    <div className="space-y-4 mt-4 w-full">
      <Accordion type="multiple" className="w-full">

        {/* Pattern Verification Layer */}
        <AccordionItem value="pattern">
          <AccordionTrigger className="text-md font-semibold">
            🧠 Pattern Detection (Stylistic Analysis)
          </AccordionTrigger>
          <AccordionContent>
            <Card className="bg-background/70 backdrop-blur-lg border-muted">
              <CardContent className="pt-4 text-sm space-y-2">
                <p><strong>Label:</strong> {pattern_verification?.label}</p>
                <p><strong>Confidence:</strong> {(pattern_verification?.confidence * 100).toFixed(2)}%</p>
                <p><strong>Reason:</strong> {pattern_verification?.reason}</p>
              </CardContent>
            </Card>
          </AccordionContent>
        </AccordionItem>

        {/* Source Credibility Layer */}
        <AccordionItem value="source">
          <AccordionTrigger className="text-md font-semibold">
            🌐 Source Credibility (Domain Check)
          </AccordionTrigger>
          <AccordionContent>
            <Card className="bg-background/70 backdrop-blur-lg border-muted">
              <CardContent className="pt-4 text-sm space-y-2">
                <p><strong>Domain:</strong> {source_credibility?.domain}</p>
                <p><strong>Credibility Rating:</strong> {source_credibility?.credibility_rating}</p>
                <p><strong>Bias:</strong> {source_credibility?.bias}</p>
                <p><strong>MBFC Score:</strong> {source_credibility?.score}</p>
                <p><strong>Note:</strong> {source_credibility?.note}</p>
                <p className="text-xs italic text-muted-foreground">{source_credibility?.reason}</p>
              </CardContent>
            </Card>
          </AccordionContent>
        </AccordionItem>

        {/* Cross Reference Layer */}
        <AccordionItem value="crossref">
          <AccordionTrigger className="text-md font-semibold">
            📚 Cross-Reference (Factual Claim Check)
          </AccordionTrigger>
          <AccordionContent>
            <Card className="bg-background/70 backdrop-blur-lg border-muted">
              <CardContent className="pt-4 text-sm space-y-2">
                <p><strong>Verdict:</strong> {cross_reference?.verdict}</p>
                <p><strong>Summary:</strong> {cross_reference?.summary}</p>
                {cross_reference?.issues?.length > 0 && (
                  <div className="mt-2 space-y-2">
                    <h4 className="font-semibold">Flagged Claims:</h4>
                    {cross_reference.issues.map((issue, idx) => (
                      <div
                        key={idx}
                        className="p-3 border rounded-md border-muted bg-muted/10"
                      >
                        <p><strong>Claim:</strong> {issue.claim}</p>
                        <p className="text-muted-foreground"><strong>Explanation:</strong> {issue.explanation}</p>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </div>
  );
};

export default ResultDetails;
