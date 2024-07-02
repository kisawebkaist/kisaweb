import { Stack, Typography } from "@mui/material";
import { Link } from "react-router-dom";
import { faHome, faQuestion } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

const QueryFallback = () => {
  return (
    <Stack
      alignItems="center"
      flexDirection="column"
      justifyContent="center"
      className="h-full gap-y-4 -translate-x-1/2 -translate-y-1/2 top-1/2 left-1/2 absolute"
    >
      <FontAwesomeIcon icon = {faQuestion} />
      <Typography variant="h1" className="text-4xl">
        Oops ! Something Happened
      </Typography>
      <Link to="/">
        <FontAwesomeIcon icon = {faHome} />
      </Link>
    </Stack>
  );
};

export default QueryFallback;
