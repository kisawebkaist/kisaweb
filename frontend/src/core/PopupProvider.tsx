import { Dialog, DialogProps } from "@mui/material";
import React, { createContext, createRef, useContext, useEffect, useRef, useState } from "react";

// Having a global dialog will prevent dialog overlapping

export type PopupContextT = {
    setDialogProps: (props: Omit<DialogProps, "open">) => void;
    show: () => void;
    hide: () => void;
};

const PopupContext = createContext<PopupContextT>(null!);

export const usePopup = () => useContext(PopupContext);

const PopupDialog = (props: {setDialogPropsRef: React.MutableRefObject<React.Dispatch<React.SetStateAction<DialogProps>>>}) => {
    const [dialogProps, setDialogPropsInner] = useState<DialogProps>({
        open: false,
    });
    props.setDialogPropsRef.current = setDialogPropsInner;

    console.log("Popup re-rendered");

    return <Dialog {...dialogProps}/>
}

export const PopupProvider = ({ children }: React.PropsWithChildren) => {
    const setDialogPropsInner = useRef<React.Dispatch<React.SetStateAction<DialogProps>>>((value)=>{});
    let dialogProps: DialogProps = {"open": false};

    const setDialogProps = (value: Omit<DialogProps, "open">) => {
        dialogProps = value as DialogProps;
        dialogProps.open = false;
        setDialogPropsInner.current(dialogProps);
    }
    const hide = () => {
        dialogProps.open = false; 
        dialogProps.onClose = () => {};
        setDialogPropsInner.current(dialogProps);
        console.log("hide working", dialogProps);
    };
    const show = () => {
        dialogProps.open = true;
        setDialogPropsInner.current(dialogProps);
        console.log("show working");
    };

    return (
        <PopupContext.Provider value={{ setDialogProps, show, hide }}>
            <PopupDialog setDialogPropsRef={setDialogPropsInner} />
            {children}
        </PopupContext.Provider>
    )
};

export default PopupProvider;