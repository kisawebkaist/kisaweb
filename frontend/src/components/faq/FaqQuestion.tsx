import {
  Stack,
  Typography,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Icon,
} from "@mui/material";
import { Box } from "@mui/system";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faA, faAdd } from "@fortawesome/free-solid-svg-icons";
import type { FaqT } from "../../API/faq";
import React from "react";

type QuestionEntry = {
  data: FaqT;
};

const FaqQuestion = ({ data }: QuestionEntry) => {
  const [isOpen, setIsOpen] = React.useState(false);
  const onOpen = React.useCallback(() => {
    setIsOpen((prevIsOpen) => !prevIsOpen);
  }, []);
  return (
    <Accordion className = "flex flex-col">
      <AccordionSummary onClick = {onOpen}>
        <Stack
          direction="row"
          alignItems="center"
          gap={2}
          className="transition-opacity ease-in rounded-lg shadow-none"
        >
          {/* <FontAwesomeIcon icon = {faAdd} color = "#0031DF"/> */}
          <Icon color="action">
            <FontAwesomeIcon
              icon={faAdd}
              className={"transition-transform " + (isOpen ? "rotate-45" : "")}
            />
          </Icon>
          <Typography variant="h4" fontWeight="bold">
            {data.question}
          </Typography>
        </Stack>
      </AccordionSummary>
      <AccordionDetails>{data.answer}</AccordionDetails>
    </Accordion>
  );
};

export default FaqQuestion;
