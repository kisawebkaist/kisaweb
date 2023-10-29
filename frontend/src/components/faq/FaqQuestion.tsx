import {
    Stack,
    Typography,
    Accordion,
    AccordionSummary,
    AccordionDetails,
  } from "@mui/material";
  import { Box } from "@mui/system";
  import AddIcon from "@mui/icons-material/Add";
  import type { FaqT } from "../../API/faq";
  
  type QuestionEntry = {
    data: FaqT;
    id: number;
  };
  
  const FaqQuestion = ({ data }: QuestionEntry) => {
    return (
      <Box my={2}>
        <Accordion>
          <AccordionSummary>
            <Stack
              direction="row"
              alignItems="center"
              gap={2}
              sx={{
                transition: "opacity 0.1s ease-in",
                "&:hover": {
                  cursor: "pointer",
                  opacity: "0.8",
                },
              }}
            >
              <AddIcon
                sx={{
                  color: "#0031DF",
                }}
              />
              <Typography variant="h6" fontWeight="bold">
                {data.question}
              </Typography>
            </Stack>
          </AccordionSummary>
          <AccordionDetails>{data.answer}</AccordionDetails>
        </Accordion>
      </Box>
    );
  };
  
  export default FaqQuestion;
  