import React, { Component } from "react";
import GridLayout from 'react-grid-layout';
import axios from 'axios';
import Dropdown from "react-dropdown";
import 'bootstrap/dist/css/bootstrap.min.css';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import './registrar.css';
import { BrowserRouter as Router,withRouter } from "react-router-dom";
import LogoutButton from "./logoutbutton"
import ViewPendingCases from './viewPendingCases.component'
import './form.css';
/**
 * props : cin,goback
 */

class AdjForm extends Component {
    constructor(props) {
        super(props);
        this.state = {
            reason: "",
            cin: props.cin ? props.cin : "",
            closed: false,
            case_summary: "",
            cin_recv:props.cin?true:false,

            reason_error: false,
            cin_error: false,
            case_summary_error: false

        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }
    handleSubmit(e) {
        e.preventDefault();
        var errors = {
            reason_error: false,
            cin_error: false
        }
        //Validate Form input
        var flag = false;
        if (this.state.reason == "") {
            this.setState({ reason_error: true });
            errors.reason_error = true;
            flag = true;
        }
        else {
            this.setState({ reason_error: false });
            errors.reason_error = false;
        }

        if (this.state.cin == "") {
            this.setState({ cin_error: true });
            errors.cin_error = true;
            flag = true;
        }
        else {
            this.setState({ cin_error: false });
            errors.cin_error = false;
        }

        if (this.state.closed) {
            if (this.state.case_summary == "") {
                this.setState({ case_summary_error: true });
                errors.case_summary_error = true;
                flag = true;
            }
            else {
                this.setState({ case_summary_error: false });
                errors.case_summary_error = false;
            }
        }
        else {
            this.setState({ case_summary_error: false });
            errors.case_summary_error = false;
        }
        //Data validation
        if(this.state.reason.includes("|"))
        {
            alert("Reason should not contain '|' ");
            flag = true;
        }
        var numbers = /^[0-9]+$/;
        if(!this.state.cin.match(numbers))
        {
            alert('CIN must be Integer')
            flag = true;
        }
        if (!flag) {
            const requestOptions = {
                'cin': this.state.cin,
                'reason': this.state.reason

            };
            axios.post('/api/addAdjournmentSummary', requestOptions)
                .then(res => {
                    console.log(res.data);
                    if (res.data.confirm == "0") {
                        alert(res.data.message);
                        if(res.data.message=="Please assign the next hearing of the case!")
                        {
                            this.props.history.push(`/assignslot/${this.state.cin}`);
                        }
                    }
                    else {

                        alert('Adjournment Details Added Successfully');
                        if (!this.state.closed) this.props.goback();
                        if (this.state.closed) {
                            const req = {
                                'cin': this.state.cin,
                                'case_summary': this.state.case_summary
                            }
                            axios.post('/api/closeCase', req)
                                .then(res => {
                                    console.log('Close Case Response', res.data);
                                    if (res.data.confirm == "0") {
                                        alert(res.data.message);
                                    }
                                    else {
                                        alert('Case ' + this.state.cin + ' was closed successfully ');
                                        this.props.goback();
                                    }
                                })
                                .catch(err => {
                                    err.response ? alert('Error in Server ' + err.response.status) : console.log(err);
                                });
                        }
                    }
                })
                .catch(err => {
                    err.response ? alert('Error in Server ' + err.response.status) : console.log(err);
                });


        }

    }
    handleChange(e) {
        
        if (e.target.name != 'case_summary') {
            this.setState({ [e.target.name]: e.target.value });
            if (e.target.value == "") {
                this.setState({ [e.target.name + "_error"]: true },()=>console.log(this.state));
                
            }
            else {
                this.setState({ [e.target.name + "_error"]: false });
                
            }
        }
        else {
            this.setState({ [e.target.name]: e.target.value });
            if (this.state.closed) {
                if (e.target.value == "") {
                    this.setState({ case_summary_error: true });
                    
                }
                else {
                    this.setState({ case_summary_error: false });
                    
                }
            }
            else {
                this.setState({ case_summary_error: false });
            }
        }
        
        
    }
    render() {
        return (
            <Router>
                <div className="Registrar">
                    <div className="Registrar-header">
                        {
                            typeof (this.props.goback) == "string" ?
                                <a href={this.props.goback}>Go Back</a>
                                : <button
                                    onClick={this.props.goback}
                                    style={{ marginLeft: "auto" }}
                                    className="btn btn-primary "
                                >
                                    Go Back
                                </button>
                        }
                        <form onSubmit={this.handleSubmit}>
                            <h3>Add Adjournment Details</h3>

                            <div className="form-group">
                                <label>Enter Reason of Adjournment: </label>
                                <input type="text" name="reason" onChange={this.handleChange} className="form-control" placeholder="Enter Adjournment Reason" />
                                {this.state.reason_error ? <div style={{ color: "red" }}>Reason cannot be Empty</div> : ""}
                            </div>

                            {
                                !this.state.cin_recv ?
                                    <div className="form-group">
                                        <label>Enter Case Identificaation Number: </label>
                                        <input type="text" name="cin" onChange={this.handleChange} className="form-control" placeholder="Enter CIN" />
                                        {this.state.cin_error ? <div style={{ color: "red" }}>CIN cannot be Empty</div> : ""}
                                    
                                    <h3>Select From Pending Cases</h3>
                                    <ViewPendingCases handleselect={(props) => { this.setState({ cin: props.data.cin,cin_recv:true });  }} />
                                    </div>
                                    : null
                            }
                            <div className="form-group">
                                <label>Close Case : </label>
                                <input type="checkbox" name="close" onChange={(e) => { this.setState({ closed: e.target.checked }, () => console.log('Check', this.state)) }} />
                            </div>

                            {
                                this.state.closed ?
                                    <div className="form-group">
                                        <label>Enter Judgement Summary: </label>
                                        <input type="text" name="case_summary" onChange={this.handleChange} className="form-control" placeholder="Enter Judgement Summary" />
                                        {this.state.case_summary_error ? <div style={{ color: "red" }}>Summary cannot be Empty</div> : ""}
                                    </div>
                                    : null
                            }

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
export default withRouter(AdjForm);