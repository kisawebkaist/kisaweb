import { Link, redirect, useNavigate } from "react-router-dom";
import {
  AppBar,
  Avatar,
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  CardHeader,
  Dialog,
  Drawer,
  IconButton,
  Stack,
  styled,
  Tab,
  Tabs,
  Toolbar,
  Tooltip,
  Typography,
} from "@mui/material";

// import MenuIcon from '@mui/icons-material/Menu';
// import MenuOpenIcon from '@mui/icons-material/MenuOpen';
// import LoginIcon from '@mui/icons-material/Login'
// import LogoutIcon from '@mui/icons-material/Logout'
// import PrivacyTipIcon from '@mui/icons-material/PrivacyTip';

import React, { useCallback, useContext, useState } from "react";
import { AuthAPI, User, UserInfo } from "../API/sso";
import { tabRoutes } from "../configs/routes";

import "../components/css/navbar.css";
import { personalInfoUsage } from "./personalInfoUsage";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faBars,
  faRightFromBracket,
  faRightToBracket,
  faShield,
  faXmark,
} from "@fortawesome/free-solid-svg-icons";
import CollapsibleIconButton from "../components/common/CollapsibleIconButton";
import { useAuth } from "./AuthContext";
import ShapeShifter from "../components/common/ShapeShifter";
import TooltipWithDisable from "../components/common/TooltipWithDisable";

export type NavbarP = {
  currentTab: string;
  setCurrentTab: React.Dispatch<React.SetStateAction<string>>;
  drawerOpen: boolean;
  setDrawerOpen: React.Dispatch<React.SetStateAction<boolean>>;
};

const AuthManager = () => {
  const [open, setOpen] = useState<boolean>(false);
  const toggleOpen = () => setOpen(!open);
  const authContext = useAuth();
  const navigate = useNavigate();
  const [dialogContent, setDialogContent] = useState<React.ReactNode>();

  if (!authContext.user.is_authenticated) {
    return (
      <CollapsibleIconButton
        color="inherit"
        startIcon={<FontAwesomeIcon icon={faRightToBracket} />}
        onClick={() => AuthAPI.login("/").then(redirect => navigate(redirect))}
        breakpoint="md"
        tooltipText={"Login"}
        tooltipEnabled={true}>
        LOGIN
      </CollapsibleIconButton>
    )
  }

  const nameAvatar = (name: string) => (
    <Avatar>{name.length === 0 ? "?" : name[0]}</Avatar>
  );
  const accountSettingsDialogContent = (
    <Card>
      <CardHeader
        avatar={nameAvatar(authContext.user.data.name)}
        title={authContext.user.data.name}
        subheader={authContext.user.data.email}
        action={
          <Tooltip title="Personal data usage notice">
            <IconButton onClick={() => setDialogContent(dataCollectionInfoDialogContent)}>
              <FontAwesomeIcon icon={faShield} />
            </IconButton>
          </Tooltip>
        }
      />
      <CardContent></CardContent>
      <CardActions>
        <Button
          color="inherit"
          onClick={() => AuthAPI.logout("/").then(redirect => navigate(redirect))}
        >
          <FontAwesomeIcon icon={faRightFromBracket} />
          Logout
        </Button>
      </CardActions>
    </Card>
    );

  const dataCollectionInfoDialogContent = (
    <Card>
      <CardHeader
        title="Personal Information Usage Disclosure"
        subheader={"Last Modified: " + personalInfoUsage.lastModified}
      />
      {personalInfoUsage.statement}
      <CardActions>
        <Button onClick={() => setDialogContent(accountSettingsDialogContent)}>
          Back
        </Button>
        <Button color="secondary">delete my account</Button>
      </CardActions>
    </Card>
  );

  return (
    <React.Fragment>
      <Tooltip title="Account Settings">
        <IconButton onClick={toggleOpen}>{nameAvatar(authContext.user.data.name)}</IconButton>
      </Tooltip>
      <Dialog open={open} onClose={() => setOpen(false)}>
        {dialogContent}
      </Dialog>
    </React.Fragment>
  );
};

const KISAIcon = (
  <Box
    component="img"
    src="/kisaLogo.png"
    alt="KISA Logo"
    height="100%"
  />
);

const Navbar = ({
  currentTab,
  setCurrentTab,
  drawerOpen,
  setDrawerOpen,
}: NavbarP) => {
  const navMenuButton = useCallback((drawerOpen: boolean) => {
    const handleOnClick = (event: React.SyntheticEvent) =>
      setDrawerOpen(!drawerOpen);
    return (
      <TooltipWithDisable disabled={drawerOpen} title="Navigation Menu">
        <IconButton color="inherit" onClick={handleOnClick}>
          {drawerOpen ? (
            <FontAwesomeIcon icon={faXmark} />
          ) : (
            <FontAwesomeIcon icon={faBars} />
          )}
        </IconButton>
      </TooltipWithDisable>
    );
  }, [setDrawerOpen]);

  const tabs = (
  <Tabs
    variant="scrollable"
    orientation="horizontal"
    scrollButtons={true}
    value={currentTab}
    onChange={(_, value) => setCurrentTab(value)}
    textColor="inherit"
    TabIndicatorProps={{sx: { backgroundColor: "var(--AppBar-color)" }}}
  >
    {tabRoutes.map((tabRoute)=>(
      <Tab 
        label={tabRoute.tabName}
        value={tabRoute.path}
        component={Link}
        to={tabRoute.path}
        key={tabRoute.path}
      />
    ))}
  </Tabs>
  );

  return (
    <AppBar position="sticky" sx={{ height: "var(--AppBar-height)" }}>
      <Toolbar sx={{ justifyContent: "space-between" }}>
        <ShapeShifter down={navMenuButton(drawerOpen)} up={KISAIcon} breakpoint="md" />
        <ShapeShifter down={KISAIcon} up={tabs} breakpoint="md" />
        <AuthManager/>
      </Toolbar>
    </AppBar>
  );
};
export default Navbar;
