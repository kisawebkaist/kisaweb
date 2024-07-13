import { Typography } from "@mui/material";

export function HighlightedLetter({ letter }: { letter: string }) {
    return (
        <Typography variant="inherit" color="primary" display="inline">
        {letter}
        </Typography>
    );
}