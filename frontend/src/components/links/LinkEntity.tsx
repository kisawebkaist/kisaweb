import {
  Stack,
  Typography,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  AccordionActions,
  Button,
  Chip,
  Icon,
} from "@mui/material";
import type { LinkT } from "../../API/links";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faAdd } from "@fortawesome/free-solid-svg-icons";
import React from "react";

type EntityEntry = {
  data: LinkT;
};

const LinkEntity = ({ data }: EntityEntry) => {
  const [isOpen, setIsOpen] = React.useState(false);
  const toggleOpen = React.useCallback(
    () => setIsOpen((prevIsOpen) => !prevIsOpen),
    []
  );
  return (
    <Accordion>
      <AccordionSummary onClick={toggleOpen}>
        <Stack direction="row" justifyContent="space-between" width="100%">
          <Stack
            direction="row"
            alignItems="center"
            gap={2}
            className="transition-opacity ease-in rounded-lg shadow-none"
          >
            <Icon color="action" className={isOpen ? "rotate-45" : ""}>
              <FontAwesomeIcon icon={faAdd} />
            </Icon>
            <Typography variant="h6" fontWeight="bold">
              {data.title}
            </Typography>
          </Stack>
          <Stack direction="row" gap={1}>
            {data.is_english && (
              <Chip
                label="English"
                className="bg-black rounded-lg text-white font-bold"
              />
            )}
            {data.requires_sso && (
              <Chip
                label="SSO Required"
                className="bg-sky-600 rounded-lg text-white font-bold"
              />
            )}
            {data.external_access && (
              <Chip
                label="SSO Required"
                className="bg-cyan-600 rounded-lg text-white font-bold"
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
  );
};

export default LinkEntity;
