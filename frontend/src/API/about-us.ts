type DivisionT = {
  division_name : string,
  id : number
}
type MemberT = {
  name : string
  image : string // Link to image basically the src
  year : string
  semester : string
  sns_link : string
  division : number // Division Primary Key
}
type InternalBoardMemberT = {
  name : string
  image : string // Link to image basically the src
  year : string
  semester : string
  sns_link : string
  position : string
  division : number
}

export default class AboutUs{
  static members = () : Promise<MemberT[]> => {
    return new Promise<MemberT[]>((res, rej) => res([]))
  }
  static internalMembers = () : Promise<InternalBoardMemberT[]> => {
    return new Promise<InternalBoardMemberT[]>((res, rej) => res([]))
  }
  static divisions = () : Promise<DivisionT[]> => {
    return new Promise<DivisionT[]>((res, rej) => res([]))
  }

}
