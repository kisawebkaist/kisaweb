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
  SvgIcon,
  IconButton,
  Tooltip,
  Box,
} from "@mui/material";
import type { LinkT } from "../../API/links";
import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faChevronDown, faArrowUpRightFromSquare, faCircleCheck, faCircleXmark} from "@fortawesome/free-solid-svg-icons";

type EntityEntry = {
  data: LinkT;
};

const LinkEntity = ({ data }: EntityEntry) => {
  const [isOpen, setIsOpen] = React.useState(false);
  const toggleOpen = React.useCallback(
    () => setIsOpen((prevIsOpen) => !prevIsOpen),
    []
  );

  const renderFlags = () => {
    const renderAvailibilityChip = (availible: boolean, label: string, className?: string) => (
      <>
        <Chip icon={availible? <FontAwesomeIcon icon={faCircleCheck}/>: <FontAwesomeIcon icon={faCircleXmark}/>} label={label} size="small" sx={{ display: {xs: 'none', sm: 'block'} }}/>
        <Tooltip title={label} sx={{ display: {xs: 'block', sm: 'none'} }}>
          <Box>{availible? <FontAwesomeIcon icon={faCircleCheck}/>: <FontAwesomeIcon icon={faCircleXmark}/>}</Box>
        </Tooltip>
      </>
    );
    return (
      <Stack
        direction="row"
        alignItems="center"
        gap={1}
      >
        {renderAvailibilityChip(data.is_english, "English", "bg-black")}
        {renderAvailibilityChip(data.requires_sso, "SSO", "bg-sky-600")}
        {renderAvailibilityChip(data.external_access, "External", "bg-cyan-600")}
      </Stack>
    );
  };
  return (
    <Accordion className = "my-2">
      <AccordionSummary 
      onClick={toggleOpen}
      expandIcon={<FontAwesomeIcon icon = {faChevronDown}/>}
      >
        <Stack direction="row" justifyContent="space-between" className = "w-full">
          <Typography alignContent="center">
            {data.title}
          </Typography>
          <IconButton href={data.url}>
            <FontAwesomeIcon icon={faArrowUpRightFromSquare} />
          </IconButton>
        </Stack>
      </AccordionSummary>
      <AccordionDetails>
      {data.description}
      <Stack direction="row" justifyContent="space-between">
        <Typography variant="subtitle1" color="gray">
          {data.url}
        </Typography>
        {renderFlags()}
      </Stack>
      </AccordionDetails>
    </Accordion>
  );
};

export default LinkEntity;
