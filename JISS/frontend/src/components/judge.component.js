import React, { Component } from "react";
import Dropdown from "react-dropdown";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import '../../node_modules/bootstrap/dist/css/bootstrap.min.css';
import './judge.css';
import LogoutButton from "./logoutbutton"
import CourtCase from "./court_case.component"
import DispCIN from './dispCIN.component'
import axios from 'axios';
import {
    useHistory,
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
    Redirect
} from "react-router-dom";

class SearchById extends Component {
    constructor(props) {
        super(props);
        this.state = { ID: "", ID_error: false };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }
    handleChange(event) {
        this.setState({ [event.target.name]: event.target.value });
        if (event.target.value == "") {
            this.setState({ [event.target.name + '_error']: true });
        }
        else {
            this.setState({ [event.target.name + '_error']: false });
        }
    }
    handleSubmit(event) {
        event.preventDefault();

        var flag = false;
        if (this.state.ID == "") {
            this.setState({ ID_error: true });
            flag = true;
        }
        else {
            this.setState({ ID_error: false });
        }
        if (!flag) {
            alert(this.state.ID + " was Submitted");
            const requestOptions = {
                'cin': this.state.ID,
            };
            axios.post('/api/searchbyId', requestOptions)
                .then(res => {
                    console.log(res.data);
                    if(res.data.confirm=="1")
                    {
                        this.props.handleviewCase(res.data.case_details); 
                    }
                    else
                    {
                        alert(res.data.message);
                    }
                                       
                })
                .catch(err => {
                    err.response ? alert('Error in Server ' + err.response.status) : console.log(err);
                });
        }



    }
    render() {
        return (
            <Router>

                <form onSubmit={this.handleSubmit}>
                    <label>
                        Enter ID:
                    <input type="text" onChange={this.handleChange} name="ID" />
                    {this.state.ID_error ? <div style={{ color: "red" }}>CIN cannot be Empty</div> : ""}
                    </label>
                    <input type="submit" value="Search" />
                </form>
            </Router>
        );
    }
}
class SearchByKey extends Component {
    constructor(props) {
        super(props);
        this.state = { Keyword: "", Keyword_error: false };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }
    handleChange(event) {
        this.setState({ [event.target.name]: event.target.value });
        if (event.target.value == "") {
            this.setState({ [event.target.name + '_error']: true });
        }
        else {
            this.setState({ [event.target.name + '_error']: false });
        }
    }
    handleSubmit(event) {
        event.preventDefault();
        var flag = false;
        if (this.state.Keyword == "") {
            this.setState({ Keyword_error: true });
            flag = true;
        }
        else {
            this.setState({ Keyword_error: false });
        }
        if (!flag) {
            alert(this.state.Keyword + " was Submitted");
            const requestOptions = {
                'key': this.state.Keyword,
            };
            axios.post('/api/searchbyKey', requestOptions)
                .then(res => {
                    console.log(res.data);
                    this.props.handleviewCaseId(res.data.cin_list);                    
                });
        }

    }
    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <label>
                    Enter Keyword:
                    <input type="text" onChange={this.handleChange} name="Keyword" />
                    {this.state.Keyword_error ? <div style={{ color: "red" }}>Keyword cannot be Empty</div> : ""}
                </label>
                <input type="submit" value="Search" />
            </form>
        );
    }
}
class Judge extends Component {
    constructor(props) {
        super(props);
        this.state = {
            name: props.name,
            comp: null, 
            curr_casedata: null, 
            searchrecv_id: false,             
            searchrecv_Key:false,
            curr_caseIdList:[]
        };
        this.OnCriteriaChange = this.OnCriteriaChange.bind(this);
        this.handleviewCase = this.handleviewCase.bind(this);
        this.handleviewCaseId = this.handleviewCaseId.bind(this);
        this.goback = this.goback.bind(this);
        this.handleviewreqCase = this.handleviewreqCase.bind(this);
    }
    handleviewreqCase(props)
    {
        console.log(props);
        alert("Getting Details for"+props.data.cin);
        const requestOptions = {
            'cin': props.data.cin,
        };
        axios.post('/api/searchbyId', requestOptions)
            .then(res => {
                console.log(res.data);
                this.handleviewCase(res.data.case_details);
            });
    }
    goback() {
        if(this.state.searchrecv_Key)
        {
            if(this.state.searchrecv_id)
            {
                this.setState({searchrecv_id: false});
            }
            else
            {
                this.setState({searchrecv_Key:false});
            }
        }
        else
        {
            this.setState({searchrecv_id:false});
        }
        
    }
    OnCriteriaChange(event) {
        if (event.target.value === "ById") {
            this.setState({ comp: <SearchById handleviewCase={this.handleviewCase} /> });
        }
        else if (event.target.value === "ByKeyword") {
            this.setState({ comp: <SearchByKey handleviewCaseId={this.handleviewCaseId} /> });
        }
        else {
            this.setState({ comp: null });
        }

    }
    
    handleviewCase(props) {
        this.setState({ searchrecv_id: true, curr_casedata: props });
        //console.log(this.state.curr_casedata);
    }
    handleviewCaseId(props) {
        /**
         * props : List of all {'cin':'<CIN>','crime_type':'<crime_type>'}
         */
        this.setState({  curr_caseIdList: props ,searchrecv_Key: true,});
        console.log('Handle View Case Judge: ',this.state.curr_caseIdList);
    }
    render() {
        
        if (this.state.searchrecv_id) {            
            return (<CourtCase case_data={this.state.curr_casedata} goback={this.goback} />);
        }
        else if (this.state.searchrecv_Key)
        {
            return (<DispCIN cin_list={this.state.curr_caseIdList} handleselect = {this.handleviewreqCase} goback ={this.goback}/>);
        }
        return (
            <Router>

                <div className="Judge">
                    <div className="Judge-header">
                        <h1>Welcome, {this.state.name}</h1>
                        <br />
                    Search Old Case:
                    <select className="Judge-dropdown-header" defaultValue="Option-Select" onChange={this.OnCriteriaChange}>
                            <option value="Option-Select" >Select An Option</option>
                            <option value="ById" >Search By ID</option>
                            <option value="ByKeyword">Search By Keyword</option>
                        </select>
                        {this.state.comp}

                        <LogoutButton handlelogout={this.props.handlelogout} />
                    </div>
                </div>
            </Router>
        );
    }
}
export default Judge;