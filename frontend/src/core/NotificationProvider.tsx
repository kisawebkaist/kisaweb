import { Snackbar, SnackbarProps } from "@mui/material";
import React, { createContext, useContext, useEffect, useRef, useState } from "react";

export type NotificationContextT = {
    setNotificationData: (noti: Notification) => void;
    showNotification: (message: String) => void;
}

export const NotificationContext = createContext<NotificationContextT>(null!);

export const useNotification = () => useContext(NotificationContext);

const NotificationSnackbar = (props: {setNotificationData: React.MutableRefObject<React.Dispatch<React.SetStateAction<SnackbarProps>>>}) => {
    const [notificationData, setNotificationDataInner] = useState<SnackbarProps>({
        message: "",
        anchorOrigin: {horizontal: "left", vertical: "bottom"},
        open: false,
        autoHideDuration: 3000,
        onClose: (event: React.SyntheticEvent | Event, reason: string) => {}
    });
    useEffect(()=>{
        props.setNotificationData.current = setNotificationDataInner;
    }, [props.setNotificationData])
    return <Snackbar {...notificationData}/>;
};

export const NotificationProvider = ({ children }: React.PropsWithChildren) => {
    const setNotificationDataInner = useRef<React.Dispatch<React.SetStateAction<SnackbarProps>>>(null!);
    const setNotificationData = setNotificationDataInner.current!;
    const showNotification = (message: String) => {
        const setNotificationDataVal = setNotificationDataInner.current!;
        setNotificationDataVal({
            message: message,
            anchorOrigin: {
            vertical: "bottom",
            horizontal: "left"
            },
            open: true,
            autoHideDuration: 3000,
            onClose: (event: React.SyntheticEvent | Event, reason: string) => {
            setNotificationDataVal({
                message: "",
                anchorOrigin: {
                vertical: "bottom",
                horizontal: "left",
                },
                open: false,
                autoHideDuration: 3000,
                onClose: (event, reason) => {
                setNotificationDataVal({
                    message: message,
                    anchorOrigin: {
                    vertical: "bottom",
                    horizontal: "left"
                    },
                    open: false,
                    autoHideDuration: 3000,
                    onClose: (event, reason) => {}
                })
                }
            })
            }
        })
    };

    return (
        <NotificationContext.Provider value={{setNotificationData, showNotification}}>
            {children}
            <NotificationSnackbar setNotificationData={setNotificationDataInner} />
        </NotificationContext.Provider>
    );
    
};

export default NotificationProvider;