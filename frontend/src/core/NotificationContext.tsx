import { SnackbarOrigin } from "@mui/material";
import { createContext, useContext } from "react";

export type Notification = {
    message: String;
    anchorOrigin: SnackbarOrigin;
    open: boolean;
    autoHideDuration: number;
    onClose: (event: React.SyntheticEvent | Event, reason: string) => void
}

export type NotificationContextT = {
    notification: Notification
    updateNotification: (noti: Notification) => void
    showNotification: (message: String) => void
}

export const defaultNotificationContext: NotificationContextT = {
    notification: {
        message: "",
        anchorOrigin: {
            vertical: "bottom",
            horizontal: "left"
        },
        open: false,
        autoHideDuration: 3000,
        onClose: (event: React.SyntheticEvent | Event, reason: string) => {}
    },
    updateNotification: (noti: Notification) => {},
    showNotification: (message: String) => {},
}

export const NotificationContext = createContext<NotificationContextT>(defaultNotificationContext);

export const useNotification = () => useContext(NotificationContext);

export default NotificationContext;