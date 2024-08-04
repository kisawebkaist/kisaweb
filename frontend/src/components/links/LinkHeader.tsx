import { Link, Typography } from "@mui/material";
import { Box } from "@mui/system";
import { HighlightedLetter } from "../common/HighlightedLetter";

const LinkHeader = () => {
  return (
    <Box component="header" textAlign="center" my={2}>
      <Typography variant="fancy_h1">
        <HighlightedLetter letter="Important "/>
        Links
      </Typography>
      <Typography variant="subtitle1">
        Want to add a new link? You can{" "}
          <Link href="/about-us">
            contact us
          </Link>
          !
      </Typography>
    </Box>
  );
};

export default LinkHeader;
