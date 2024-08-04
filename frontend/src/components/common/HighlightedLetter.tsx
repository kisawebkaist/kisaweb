import { Typography } from "@mui/material";

export const HighlightedLetter = ({ letter }: { letter: string }) => (
    <Typography variant="inherit" color="primary" display="inline">
        {letter}
    </Typography>
);

export default HighlightedLetter;
