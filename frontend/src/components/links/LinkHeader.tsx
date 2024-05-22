import { Typography } from "@mui/material";
import { Box } from "@mui/system";

const LinkHeader = () => {
  return (
    <Box component="header" textAlign="center" my={2}>
      <Typography variant="h3">
        <HighlightedLetter letter="Important " />
        Links
      </Typography>
      <Typography variant="subtitle1" color="#969696">
        Want to add a new link? You can{" "}
        <Typography display="inline" color="#3D5FDA" style={{ textDecoration: "none" }}>
          <a style={{ textDecoration: "none" }} href="/about-us">
            contact us
          </a>
          !
        </Typography>
      </Typography>
    </Box>
  );
};

function HighlightedLetter({ letter }: { letter: string }) {
  return (
    <Typography variant="inherit" color={"primary"} display="inline">
      {letter}
    </Typography>
  );
}

export default LinkHeader;
