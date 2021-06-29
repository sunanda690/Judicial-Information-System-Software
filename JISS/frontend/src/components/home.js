import LogoutButton from "./logoutbutton"

export default function Home(props) {
    return (
        <div>
            <h1>Welcome to Judiciary Management System, {props.user}</h1>
            {props.isLoggedIn=="Yes"?<LogoutButton handlelogout={props.handlelogout}/>:null}
            
        </div>
    );
}