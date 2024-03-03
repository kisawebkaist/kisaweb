import React from "react";
import { DivisionT, MemberT } from "../../API/about-us";
import { Box, Stack, Typography } from "@mui/material";
import { ChartMember } from "./ChartMember";
import { Link } from "react-router-dom";

interface ChartDivisionProps extends React.PropsWithChildren {
  division: DivisionT;
  headMember: MemberT;
  members: MemberT[];
}

export function ChartDivision(props: ChartDivisionProps) {
  return (
    <Stack
      direction="column"
      // gap={1}
      justifyContent="center"
      alignItems="center"
      mb={1}
    >
      <Link
        to={`/about-us/division/${props.division.id}`}
        style={{
          textDecoration: "none",
        }}
      >
        <Box
          className="hoverable"
          sx={{
            backgroundColor: "#001F58",
            borderRadius: 2,
            p: 1,
            height: 50,
            width: 250,
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <Typography textAlign="center" color="white" fontWeight="bold">
            {props.division.division_name}
          </Typography>
        </Box>
      </Link>
      <ChartMember
        chartMember={{ ...props.headMember, position: "Division Head" }}
      />
      <Box
        sx={{
          backgroundColor: "#455B8D",
          width: 275,
          borderRadius: 2,
          textAlign: "center",
        }}
      >
        <Stack direction="column" gap={1}>
          {props.members.map((member, index) => {
            const textColor = index % 2 === 0 ? "white" : "#C2C2C2";
            return (
              <Typography key={index} m={1} color={textColor} fontWeight="bold">
                {member.name}
              </Typography>
            );
          })}
        </Stack>
      </Box>
    </Stack>
  );
}
