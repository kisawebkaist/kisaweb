import React from "react";
import { InternalBoardMemberT } from "../../API/about-us";
import {
  Avatar,
  Box,
  Card,
  CardActionArea,
  CardContent,
  Stack,
  Typography,
} from "@mui/material";

interface ChartMemberProps extends React.PropsWithChildren {
  chartMember: InternalBoardMemberT;
}

export function ChartMember(props: ChartMemberProps) {
  return (
      <Card
        variant="outlined"
        sx={{
          border: "none",
        }}
      >
        <CardActionArea>
          <Box
            sx={{
              display: "flex",
              justifyContent: "center",
            }}
          >
            <Avatar
              src={props.chartMember?.image || "https://i.insider.com/602ee9ced3ad27001837f2ac?width=700"}
              alt={props.chartMember?.name || "Rick Astley"}
              sx={{
                width: "75%",
                height: "75%",
                maxWidth: "16vw",
                maxHeight: "16vw",
                top: "1vw"
              }}
            />
          </Box>
          <CardContent
            sx={(theme) => ({
              p: "2vw",
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
              backgroundColor: theme.palette.primary.main,
            })}
          >
              <Typography
                textAlign="center"
                variant="h4"
                sx={(theme)=> ({
                  backgroundColor: theme.palette.background.paper,
                  px: "1vw"
                })}
              >
                {"Rick Roller"}
              </Typography>
          </CardContent>
        </CardActionArea>
      </Card>
  );
}
