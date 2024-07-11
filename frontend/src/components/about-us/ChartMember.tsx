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
    <Stack
      direction="column"
      justifyContent="center"
      alignItems="center"
      gap={1}
      m={1}
    >
      <Card
        variant="outlined"
        sx={{
          border: "none",
          width: 275,
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
                width: 96,
                height: 96,
                zIndex: 10,
              }}
            />
          </Box>
          <CardContent
            sx={{
              backgroundColor: "#324B79",
              p: 3,
              position: "relative",
              top: -20,
              zIndex: 0,
              borderRadius: 2,
              height: 100,
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <Box
              sx={{
                height: 70,
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              <Typography
                textAlign="center"
                variant="h3"
                color="white"
                textTransform="uppercase"
                fontWeight="bold"
              >
                {props.chartMember?.name || "Rick Astley"}
              </Typography>
            </Box>
            <Box
              sx={{
                backgroundColor: "#74B9FF",
                px: 1,
                borderRadius: 2,
              }}
            >
              <Typography
                textAlign="center"
                variant="h4"
                textTransform="uppercase"
                fontWeight="bold"
              >
                {props.chartMember?.position || "Rick Roller"}
              </Typography>
            </Box>
          </CardContent>
        </CardActionArea>
      </Card>
      {props.children ? (
        <Stack direction="row" gap={5}>
          {props.children}
        </Stack>
      ) : (
        <></>
      )}
    </Stack>
  );
}
