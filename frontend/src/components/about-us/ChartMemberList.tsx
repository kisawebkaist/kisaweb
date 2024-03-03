import { MemberT } from "../../API/about-us";

interface ChartMemberListProps {
  members: MemberT[];
}

export function ChartMemberList(props: ChartMemberListProps) {
  return (
    <div>
      {props.members.map((member, index) => (
        <div key={index}>
          <p>{member.name}</p>
        </div>
      ))}
    </div>
  );
}
