import NavEntryT, { NavDropdownT, NavLinkT, UserInfo } from "./types"
import Lister from "../components/lister"
import { AppBar, Avatar, Box, Button, Container, CssBaseline, Divider, Drawer, IconButton, Stack, Tab, Tabs, Toolbar, Typography } from "@mui/material";
import MenuIcon from '@mui/icons-material/Menu'
import { Link, Link as RouterLink, useLocation } from 'react-router-dom';
import "../components/css/navbar.css"

import fakeNavbarData from "./fakeDataForNavbar";
import React, { useState } from "react";
import { AuthAPI } from "../API/sso";

export class NavbarP {
  entries: NavLinkT[];
  userInfo: UserInfo;
  compactMode: boolean;

  constructor(entries: NavLinkT[] = fakeNavbarData, userInfo: UserInfo = new UserInfo(), compactMode: boolean = false) {
    this.entries = entries;
    this.userInfo = userInfo;
    this.compactMode = compactMode;
  }
}

const RenderLink = (data: NavLinkT, index: number) => <Tab label={data.data.text} value={index} component={Link} to={data.data.href}/>;

const RenderAuthMenu = ({ isAuthenticated, detail }: UserInfo) => 
    (isAuthenticated)?
        <Avatar>{ (detail==null)? "?": detail.name[0] }</Avatar>:
        <Button
            variant="contained"
            onClick={() => AuthAPI.login("/").then(redirect => window.location.href = redirect)}>
            LOGIN
        </Button>

const Navbar = ({ entries, userInfo, compactMode }: NavbarP) => {
  const navbarHeight = "75px";
  const [tabContextVal, setTabContextVal] = useState<number>(0);
  const [drawerisOpen, setDrawerState] = useState<boolean>(false);
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => setTabContextVal(newValue);
  const handleDrawerMenuOnClick = (event:React.SyntheticEvent) => setDrawerState(!drawerisOpen);

  return (
    <Stack>
    <AppBar sx={{ zIndex: (theme) => theme.zIndex.drawer + 1, height: navbarHeight}}>
        <Toolbar sx={{ justifyContent: 'space-between' }}>
            {
                compactMode ?
                <IconButton size="large" edge="start" aria-label="menu" onClick={handleDrawerMenuOnClick}>
                <MenuIcon />
                </IconButton> : null
            }
            <Box
                component="img"
                src="/kisaLogo.png"
                alt="KISA Logo"
                sx={{ height: '100%'}}
            />
            {
                compactMode ? null :
                <Tabs value={tabContextVal} onChange={handleTabChange}>
                    {entries.map(RenderLink)}
                </Tabs>
            }
            {RenderAuthMenu(userInfo)}
        </Toolbar>
    </AppBar>
    {
        compactMode? 
        <Drawer open={drawerisOpen} PaperProps={{ sx: {bgColor: 'primary.main', marginTop: navbarHeight} }} sx={{ flexShrink: 0 }}>
            <Tabs value={tabContextVal} orientation="vertical" onChange={handleTabChange}>
                {entries.map(RenderLink)}
            </Tabs>
        </Drawer> : null
    }
    </Stack>
    );
}
export default Navbar