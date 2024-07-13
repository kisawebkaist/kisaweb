import { Typography } from "@mui/material";
import { Box } from "@mui/system";
import { HighlightedLetter } from "../../core/components";

const FaqHeader = () => {
  return (
    <Box component="header" textAlign="center" my={2}>
      <Typography variant="fancy_h1">
        <HighlightedLetter letter="F" />
        requently <HighlightedLetter letter="A" />
        sked <HighlightedLetter letter="Q" />
        uestions
      </Typography>
      <Typography variant="subtitle1" color="#969696">
        Can't find the answer you are looking? You can{" "}
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

export default FaqHeader;
