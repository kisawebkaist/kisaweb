import { Link, Typography } from "@mui/material";
import { Box } from "@mui/system";

const LinkHeader = () => {
  return (
    <Box component="header" textAlign="center" my={2}>
      <Typography variant="h3">
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

function HighlightedLetter({ letter }: { letter: string }) {
  return (
    <Typography variant="inherit" color="primary" display="inline">
      {letter}
    </Typography>
  );
}

export default LinkHeader;
