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
import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faAdd } from "@fortawesome/free-solid-svg-icons";

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
    <Accordion className = "my-2">
      <AccordionSummary onClick={toggleOpen}>
        <Stack direction="row" justifyContent="space-between" className = "w-full">
          <Stack
            direction="row"
            alignItems="center"
            className="transition-opacity ease-in rounded-lg shadow-none max-w-2/3 gap-x-2"
          >
            <FontAwesomeIcon icon = {faAdd} className={isOpen ? "rotate-45" : ""} />
            <Typography variant="h6" fontWeight="bold">
              {data.title}
            </Typography>
          </Stack>
          <Stack
            direction="row"
            flexWrap="wrap"
            justifyContent="flex-end"
            alignItems="center"
            className = "max-w-1/3 gap-x-0.5 gap-y-0.5"
          >
            {data.is_english && (
              <Chip
                label="English"
                className="bg-black rounded-lg text-white font-bold"
              />
            )}
            {data.requires_sso && (
              <Chip
                label="SSO"
                className="bg-sky-600 rounded-lg text-white font-bold"
              />
            )}
            {data.external_access && (
              <Chip
                label="External"
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
