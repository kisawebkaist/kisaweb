import {
  Stack,
  Typography,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  AccordionActions,
  Button,
  Chip,
} from "@mui/material";
import { Box } from "@mui/system";
import AddIcon from "@mui/icons-material/Add";
import type { LinkT } from "../../API/links";

type EntityEntry = {
  data: LinkT;
};

const LinkEntity = ({ data }: EntityEntry) => {
  return (
    <Box my={2}>
      <Accordion>
        <AccordionSummary>
          <Stack direction="row" justifyContent="space-between" width="100%">
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
                {data.title}
              </Typography>
            </Stack>
            <Stack direction="row" gap={1}>
              {data.is_english && (
                <Chip
                  label="English"
                  sx={{
                    backgroundColor: "#343A40",
                    color: "white",
                    fontSize: "0.6rem",
                  }}
                />
              )}
              {data.requires_sso && (
                <Chip
                  label="SSO Required"
                  sx={{
                    backgroundColor: "#007BFF",
                    color: "white",
                    fontSize: "0.6rem",
                  }}
                />
              )}
              {data.external_access && (
                <Chip
                  label="Accessible off-campus"
                  sx={{
                    backgroundColor: "#17A2B8",
                    color: "white",
                    fontSize: "0.6rem",
                  }}
                />
              )}
            </Stack>
          </Stack>
        </AccordionSummary>
        <AccordionDetails>{data.description}</AccordionDetails>
        <AccordionActions>
          <Typography variant="subtitle1" color="gray">
            {data.url}
          </Typography>
          <Button variant="contained" href={data.url}>
            Visit
          </Button>
        </AccordionActions>
      </Accordion>
    </Box>
  );
};

export default LinkEntity;
