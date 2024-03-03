import React from "react";
import { DivisionT, InternalBoardMemberT, MemberT } from "../../API/about-us";
import { ChartDivision } from "./ChartDivision";
import { ChartMember } from "./ChartMember";
import { Box, Stack } from "@mui/material";

interface ChartProps {
  divisions: DivisionT[];
  members: MemberT[];
  internalBoardMembers: InternalBoardMemberT[];
}

export function Chart(props: ChartProps) {
  const president = React.useMemo(
    () =>
      props.internalBoardMembers.find(
        (member) => member.position === "President"
      )!,
    [props.internalBoardMembers]
  );
  const vicePresident = React.useMemo(
    () =>
      props.internalBoardMembers.find(
        (member) => member.position === "Vice President"
      )!,
    [props.internalBoardMembers]
  );
  const secretary = React.useMemo(
    () =>
      props.internalBoardMembers.find(
        (member) => member.position === "Secretary"
      )!,
    [props.internalBoardMembers]
  );

  return (
    <Box my={2}>
      {/* Internal board */}
      <ChartMember chartMember={president}>
        <ChartMember chartMember={vicePresident} />
        <ChartMember chartMember={secretary} />
      </ChartMember>

      {/* Divisions */}
      <Stack direction="row" justifyContent="space-around">
        {props.divisions.map((division, index) => {
          const head = props.members.find(
            (member) => member.id === division.head_member_id
          )!;
          const members = props.members.filter(
            (member) => member.division === division.id
          );
          return (
            <ChartDivision
              key={index}
              division={division}
              headMember={{ ...head }}
              members={members}
            />
          );
        })}
      </Stack>
    </Box>
  );
}
