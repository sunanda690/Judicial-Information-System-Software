import React, { Component } from "react";
import GridLayout from 'react-grid-layout';
import axios from 'axios';
import Dropdown from "react-dropdown";
import 'bootstrap/dist/css/bootstrap.min.css';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import './registrar.css';
import { BrowserRouter as Router } from "react-router-dom";
import LogoutButton from "./logoutbutton"
import './form.css';
/**
 * props : hearing_slot,hearing_date,goback
 */
export default class AddCase extends Component {
    constructor(props) {
        super(props);
        this.state = {
            def_name: "",
            def_addr: "",
            crime_type: "",
            crime_date: null,
            crime_loc: "",
            arresting_off_name: "",
            arrest_date: null,
            name_pres_judge: "",
            public_prosecutor_name: "",
            public_prosecutor_addr: "",
            starting_date: null,
            expected_completion_date: null,
            hearing_slot: props.hearing_slot ? props.hearing_slot : "-1",
            hearing_date: props.hearing_date ? props.hearing_date : null,

            def_name_error: false,
            def_addr_error: false,
            crime_type_error: false,
            crime_date_error: false,
            crime_loc_error: false,
            arresting_off_name_error: false,
            arrest_date_error: false,
            name_pres_judge_error: false,
            public_prosecutor_name_error: false,
            public_prosecutor_addr_error: false,
            starting_date_error: false

        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }
    handleSubmit(e) {
        e.preventDefault();
        var errors = {
            def_name_error: false,
            def_addr_error: false,
            crime_type_error: false,
            crime_date_error: false,
            crime_loc_error: false,
            arresting_off_name_error: false,
            arrest_date_error: false,
            name_pres_judge_error: false,
            public_prosecutor_name_error: false,
            public_prosecutor_addr_error:false,
            starting_date_error: false,

        }
        //Validate Form input
        var flag = false;
        if (this.state.def_name == "") {
            this.setState({ def_name_error: true });
            errors.def_name_error = true;
            flag = true;
        }
        else {
            this.setState({ def_name_error: false });
            errors.def_name_error = false;
        }

        if (this.state.public_prosecutor_name == "") {
            this.setState({ public_prosecutor_name_error: true });
            errors.public_prosecutor_name_error = true;
            flag = true;
        }
        else {
            this.setState({ public_prosecutor_name_error: false });
            errors.public_prosecutor_name_error = false;
        }

        if (this.state.public_prosecutor_addr == "") {
            this.setState({ public_prosecutor_addr_error: true });
            errors.public_prosecutor_addr_error = true;
            flag = true;
        }
        else {
            this.setState({ public_prosecutor_addr_error: false });
            errors.public_prosecutor_addr_error = false;
        }

        if (this.state.def_addr == "") {
            this.setState({ def_addr_error: true });
            errors.def_addr_error = true;
            flag = true;
        }
        else {
            this.setState({ def_addr_error: false });
            errors.def_addr_error = false;
        }

        if (this.state.arresting_off_name == "") {
            this.setState({ arresting_off_name_error: true });
            errors.arresting_off_name_error = true;
            flag = true;
        }
        else {
            this.setState({ arresting_off_name_error: false });
            errors.arresting_off_name_error = false;
        }

        if (this.state.name_pres_judge == "") {
            this.setState({ name_pres_judge_error: true });
            errors.name_pres_judge_error = true;
            flag = true;
        }
        else {
            this.setState({ name_pres_judge_error: false });
            errors.name_pres_judge_error = false;
        }

        

        if (this.state.crime_type == "") {
            this.setState({ crime_type_error: true });
            errors.crime_type_error = true;
            flag = true;
        }
        else {
            this.setState({ crime_type_error: false });
            errors.crime_type_error = false;
        }

        if (this.state.crime_loc == "") {
            this.setState({ crime_loc_error: true });
            errors.crime_loc_error = true;
            flag = true;
        }
        else {
            this.setState({ crime_loc_error: false });
            errors.crime_loc_error = false;
        }

        if (this.state.arrest_date == null) {
            this.setState({ arrest_date_error: true });
            errors.arrest_date_error = true;
            flag = true;
        }
        else {
            this.setState({ arrest_date_error: false });
            errors.arrest_date_error = false;
        }

        if (this.state.crime_date == null) {
            this.setState({ crime_date_error: true });
            errors.crime_date_error = true;
            flag = true;
        }
        else {
            this.setState({ crime_date_error: false });
            errors.crime_date_error = false;
        }

        if (this.state.starting_date == null) {
            this.setState({ starting_date_error: true });
            errors.starting_date_error = true;
            flag = true;
        }
        else {
            this.setState({ starting_date_error: false });
            errors.starting_date_error = false;
        }

        //Some data consistency checks
        if(this.state.crime_date>this.state.arrest_date)
        {
            alert('Crime date cannot be after arrest date');
            flag = true;
        }
        if(this.state.hearing_date && this.state.hearing_date<this.state.arrest_date)
        {
            alert('Arrest Date cannot be after hearing date');
            flag = true;
        }        
        if(this.state.hearing_date && this.state.starting_date>this.state.hearing_date)
        {
            alert('Starting Date cannot be After hearing date');
            flag = true;
        }
        
        if (!flag) {
            const requestOptions = {
                'def_name': this.state.def_name,
                'def_addr': this.state.def_addr,
                'crime_type': this.state.crime_type,
                'crime_date': {
                    'day': this.state.crime_date.getDate().toString(),
                    'month': (this.state.crime_date.getMonth()+1).toString(),
                    'year': this.state.crime_date.getFullYear().toString()
                },
                'crime_loc': this.state.crime_loc,
                'arresting_off_name': this.state.arresting_off_name,
                'arrest_date': {
                    'day': this.state.arrest_date.getDate().toString(),
                    'month': (this.state.arrest_date.getMonth()+1).toString(),
                    'year': this.state.arrest_date.getFullYear().toString()
                },
                'name_pres_judge': this.state.name_pres_judge,
                'public_prosecutor_name': this.state.public_prosecutor_name,
                'public_prosecutor_addr': this.state.public_prosecutor_addr,
                'starting_date': {
                    'day': this.state.starting_date.getDate().toString(),
                    'month': (this.state.starting_date.getMonth()+1).toString(),
                    'year': this.state.starting_date.getFullYear().toString()
                },
                'expected_completion_date': this.state.expected_completion_date ? {
                    'day': this.state.expected_completion_date.getDate().toString(),
                    'month': (this.state.expected_completion_date.getMonth()+1).toString(),
                    'year': this.state.expected_completion_date.getFullYear().toString()
                } : "-1",
                'hearing_slot': this.state.hearing_slot ? this.state.hearing_slot : "-1",
                'hearing_date': this.state.hearing_date ? {
                    'day': this.state.hearing_date.getDate().toString(),
                    'month': (this.state.hearing_date.getMonth()+1).toString(),
                    'year': this.state.hearing_date.getFullYear().toString()
                } : "-1"

            };
            axios.post('/api/addCase', requestOptions)
                .then(res => {
                    console.log(res.data);
                    if (res.data.is_added == "0") {
                        alert(res.data.message);
                    }
                    else {
                        if(this.props.getAddedCIN!=null) this.props.getAddedCIN(res.data.cin) 
                        alert('Case Added Successfully');
                        // this.props.goback();//Optional
                    }
                })
                .catch(err => {
                    err.response ? alert('Error in Server ' + err.response.status) : console.log(err);
                });
        }

    }
    handleChange(e) {
        this.setState({ [e.target.name]: e.target.value });
        if (e.target.value == "") {
            this.setState({ [e.target.name + "_error"]: true });
        }
        else {
            this.setState({ [e.target.name + "_error"]: false });
        }
    }
    render() {
        return (
            <Router>
                <div className="Registrar">
                    <div className="Registrar-header">
                        <button
                            onClick={this.props.goback}
                            style={{ marginLeft: "auto" }}
                            className="btn btn-primary "
                        >
                            Go Back
                    </button>
                        <form onSubmit={this.handleSubmit}>
                            <h3>Add Case</h3>

                            <div className="form-group">
                                <label>Defenent Name</label>
                                <input type="text" name="def_name" onChange={this.handleChange} className="form-control" placeholder="Enter Def Name" />
                                {this.state.def_name_error ? <div style={{ color: "red" }}>Name cannot be Empty</div> : ""}
                            </div>
                            <div className="form-group">
                                <label>Defendent Address</label>
                                <input type="text" name="def_addr" onChange={this.handleChange} className="form-control" placeholder="Enter Def Address" />
                                {this.state.def_addr_error ? <div style={{ color: "red" }}>Address cannot be Empty</div> : ""}
                            </div>
                            <div className="form-group">
                                <label>Crime Type</label>
                                <input type="text" name="crime_type" onChange={this.handleChange} className="form-control" placeholder="Enter Crime Type" />
                                {this.state.crime_type_error ? <div style={{ color: "red" }}>Crime Type cannot be Empty</div> : ""}
                            </div>

                            <div className="form-group">
                                Enter Crime Date: <DatePicker dateFormat="dd-MM-y" selected={this.state.crime_date} onChange={date => {
                                    this.setState({ crime_date: date });
                                    (!date) ? this.setState({ crime_date_error: true }) : this.setState({ crime_date_error: false });
                                }} />
                                {this.state.crime_date_error ? <div style={{ color: "red" }}>Crime Date cannot be Empty</div> : ""}
                            </div>

                            <div className="form-group">
                                <label>Crime Location</label>
                                <input type="text" name="crime_loc" onChange={this.handleChange} className="form-control" placeholder="Enter Crime Location" />
                                {this.state.crime_loc_error ? <div style={{ color: "red" }}>Crime Location cannot be Empty</div> : ""}
                            </div>


                            <div className="form-group">
                                <label>Arresting Officer Name: </label>
                                <input type="text" name="arresting_off_name" onChange={this.handleChange} className="form-control" placeholder="Enter Arresting Officer Name" />
                                {this.state.arresting_off_name_error ? <div style={{ color: "red" }}>Name cannot be Empty</div> : ""}
                            </div>

                            <div className="form-group">
                                Enter Arrest Date: <DatePicker dateFormat="dd-MM-y" selected={this.state.arrest_date} onChange={date => {
                                    this.setState({ arrest_date: date });
                                    (!date) ? this.setState({ arrest_date_error: true }) : this.setState({ arrest_date_error: false });
                                }} />
                                {this.state.arrest_date_error ? <div style={{ color: "red" }}>Arrest Date cannot be Empty</div> : ""}
                            </div>

                            <div className="form-group">
                                <label>Presiding Judge Name: </label>
                                <input type="text" name="name_pres_judge" onChange={this.handleChange} className="form-control" placeholder="Enter Presiding Judge Name" />
                                {this.state.name_pres_judge_error ? <div style={{ color: "red" }}>Name cannot be Empty</div> : ""}
                            </div>
                            
                            <div className="form-group">
                                <label>Public Prosecutor Name: </label>
                                <input type="text" name="public_prosecutor_name" onChange={this.handleChange} className="form-control" placeholder="Enter Public Prosecutor Name" />
                                {this.state.public_prosecutor_name_error ? <div style={{ color: "red" }}>Name cannot be Empty</div> : ""}
                            </div>

                            <div className="form-group">
                                <label>Public Prosecutor Address: </label>
                                <input type="text" name="public_prosecutor_addr" onChange={this.handleChange} className="form-control" placeholder="Enter Public Prosecutor Address" />
                                {this.state.public_prosecutor_addr_error ? <div style={{ color: "red" }}>Address cannot be Empty</div> : ""}
                            </div>

                            

                            <div className="form-group">
                                Starting Date: <DatePicker dateFormat="dd-MM-y" selected={this.state.starting_date} onChange={date => {
                                    this.setState({ starting_date: date });
                                    (!date) ? this.setState({ starting_date_error: true }) : this.setState({ starting_date_error: false });
                                }} />
                                {this.state.starting_date_error ? <div style={{ color: "red" }}>Starting Date cannot be Empty</div> : ""}
                            </div>

                            <div className="form-group">
                                Expected Completion Date: <DatePicker dateFormat="dd-MM-y" selected={this.state.expected_completion_date} onChange={date => {
                                    this.setState({ expected_completion_date: date });
                                }} />
                            </div>

                            <div className="form-group">
                                <button type="submit" className="btn btn-primary btn-block">Submit</button>
                            </div>
                        </form>
                    </div>
                </div>
            </Router>
        );
    }
}