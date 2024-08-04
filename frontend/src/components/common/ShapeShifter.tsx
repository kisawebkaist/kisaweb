import { useTheme } from "@mui/material";
import { Breakpoint, useMediaQuery } from "@mui/material";

export type ShapeShifterProps<Down extends React.ReactNode, Up extends React.ReactNode> = {
    down: Down;
    up: Up;
    breakpoint: Breakpoint
};


/**
 * 
 * A component to switch between two `ReactNode`s according to a theme breakpoint
 */
export const ShapeShifter = <Down extends React.ReactNode, Up extends React.ReactNode> (props: ShapeShifterProps<Down, Up>) => {
    const theme = useTheme();
    if (useMediaQuery(theme.breakpoints.down(props.breakpoint))) {
        return props.down;
    }
    return props.up;
};

export default ShapeShifter;