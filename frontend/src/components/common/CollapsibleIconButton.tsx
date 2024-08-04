import { Breakpoint, Button, ButtonProps, Stack, StackProps, styled, Tooltip } from "@mui/material";

export type CollapsibleIconButtonProps = ButtonProps<typeof Button, { breakpoint: Breakpoint, tooltipText: string, tooltipEnabled: boolean }>;

const CollapsibleIconButtonCollaspible = styled(Stack, {
    shouldForwardProp: (prop) => prop !== 'breakpoint'
})<StackProps<'div', { breakpoint: Breakpoint }>>(({ theme, breakpoint }) => ({
    [theme.breakpoints.down(breakpoint)]: {
        display: 'none'
    },
}));

export const CollapsibleIconButton = (props: CollapsibleIconButtonProps) => {
    let { breakpoint, children, tooltipEnabled, tooltipText, ...other } = props;
    let main = (
        <Button {...other}>
            <CollapsibleIconButtonCollaspible breakpoint={props.breakpoint}>{children}</CollapsibleIconButtonCollaspible>
        </Button>
        );
    if (tooltipEnabled) {
        main = (
            <Tooltip title={tooltipText}>
                {main}
            </Tooltip>
        )
    }
    return main;
}

export default CollapsibleIconButton;