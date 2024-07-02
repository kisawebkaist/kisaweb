import {
  Stack,
  Typography,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from "@mui/material";
import type { FaqT } from "../../API/faq";
import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faAdd } from "@fortawesome/free-solid-svg-icons";

type QuestionEntry = {
  data: FaqT;
};

const FaqQuestion = ({ data }: QuestionEntry) => {
  const [isOpen, setIsOpen] = React.useState(false);
  const onOpen = React.useCallback(() => {
    setIsOpen((prevIsOpen) => !prevIsOpen);
  }, []);
  return (
    <Accordion className="flex flex-col">
      <AccordionSummary onClick={onOpen}>
        <Stack
          direction="row"
          alignItems="center"
          gap={2}
          className="transition-opacity ease-in rounded-lg shadow-none"
        >
          <FontAwesomeIcon icon={faAdd} className={isOpen ? "rotate-45" : ""} />
          <Typography variant="h6" fontWeight="bold">
            {data.question}
          </Typography>
        </Stack>
      </AccordionSummary>
      <AccordionDetails>{data.answer}</AccordionDetails>
    </Accordion>
  );
};

export default FaqQuestion;
