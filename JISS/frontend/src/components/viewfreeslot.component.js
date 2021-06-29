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
import AddCase from './createcase.component';
import { PropertyKeys } from "ag-grid-community";
import ViewPendingCases from "./viewPendingCases.component";
import AdjForm from './enterAdjDetails.component';

class DispSlots extends Component {
    /**
     * @param: props : {handleSelectSlot, free_slot:{slot1: "1",...}}
     */
    constructor(props) {
        super(props);
        this.state = {
            selected_slot: "None",
            selected_slot_error: false
        };

        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);

    }
    handleChange(e) {
        console.log("Handle Change", e.target.value);
        this.setState({ selected_slot: e.target.value }, () => {
            if (this.state.selected_slot == "None") {
                this.setState({ selected_slot_error: true }, () => console.log("State", this.state));
            }
            else {
                this.setState({ selected_slot_error: false }, () => console.log("State", this.state));
            }
        });


    }
    handleSubmit(e) {
        e.preventDefault();
        var errors = {
            selected_slot_error: false
        }
        //Validate Form input
        var flag = false;
        if (this.state.selected_slot == "None") {
            this.setState({ selected_slot_error: true });
            errors.selected_slot_error = true;
            flag = true;
        }
        else {
            this.setState({ selected_slot_error: false });
            errors.selected_slot_error = false;
        }

        if (!flag) {
            this.props.handleSelectSlot({ 'selected_slot': this.state.selected_slot });
        }

    }
    render() {
        return (
            <div>
                <button
                    onClick={this.props.goback}
                    style={{ marginLeft: "auto" }}
                    className="btn btn-primary "
                >
                    Go Back
                </button>
                <form onSubmit={this.handleSubmit} >
                    <div className="form-group">
                        <label>Select Slot:</label>
                        <label>
                            <select className="form-control" defaultValue="None" name="usr_type" onChange={this.handleChange}>
                                <option value="None">Select Slot</option>
                                {this.props.free_slot.slot1 == "1" ? <option value="slot1">Slot 1</option> : null}
                                {this.props.free_slot.slot2 == "1" ? <option value="slot2">Slot 2</option> : null}
                                {this.props.free_slot.slot3 == "1" ? <option value="slot3">Slot 3</option> : null}
                                {this.props.free_slot.slot4 == "1" ? <option value="slot4">Slot 4</option> : null}
                                {this.props.free_slot.slot5 == "1" ? <option value="slot5">Slot 5</option> : null}
                            </select>
                            {this.state.selected_slot_error ? <div style={{ color: "red" }}>Selected Slot cannot be Empty</div> : ""}
                        </label>
                    </div>
                    <div className="form-group">
                        <button type="submit" className="btn btn-primary btn-block">Submit</button>
                    </div>
                </form>
            </div>
        );
    }
}
/**
 * props : cin,goback
 */
export default class ViewFreeSlot extends Component {
    constructor(props) {
        super(props);
        console.log('View Free Slot')
        this.state = {
            val: "0",
            free_slot: null,
            query_date: new Date(),
            pending_case_list: [],
            selected_slot: null,
            query_date_error: false,
            selected_cin: props.match ? props.match.params.cin : ""
        };
        console.log(props.location);
        console.log(this.state);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.setPendingCases = this.setPendingCases.bind(this);
        this.handleSelectSlot = this.handleSelectSlot.bind(this);
        this.handleAssignHearingDate = this.handleAssignHearingDate.bind(this);
        this.goback = this.goback.bind(this);
    }
    handleAssignHearingDate() {
        console.log('Assign Hearing Date');


        var req = {
            "cin": this.state.selected_cin,
            "slot": (
                this.state.selected_slot == "slot1" ? "1"
                    : this.state.selected_slot == "slot2" ? "2"
                        : this.state.selected_slot == "slot3" ? "3"
                            : this.state.selected_slot == "slot4" ? "4"
                                : "5"
            ),
            "date": {
                "day": this.state.query_date.getDate().toString(),
                "month": (this.state.query_date.getMonth() + 1).toString(),
                "year": this.state.query_date.getFullYear().toString()

            }
        }
        axios.post('/api/assignHearingSlot', req)
            .then(res => {
                if (res.data.confirm == "0") {
                    alert(res.data.message);
                }
                else {
                    alert("Hearing for Case with CIN " + this.state.selected_cin + "sheduled for " + this.state.query_date + ", at slot," + this.state.selected_slot);

                }
            })
            .catch(err => {
                err.response ? alert('Error in Server ' + err.response.status) : console.log(err);
            });

    }
    goback() {
        //REset the state
        this.setState({ val: "0", selected_slot: null });
    }
    handleSelectSlot(props) {
        console.log('Handle Select Slots ', props);
        if (this.state.selected_cin == "") {
            this.setState({ selected_slot: props.selected_slot }, () => { console.log(this.state); this.setState({ val: "2" }) });
        }
        else {
            this.setState({ selected_slot: props.selected_slot }, () => { console.log(this.state); this.handleAssignHearingDate(); });
            this.setState({ val: "4" });
        }


    }
    setPendingCases(props) {
        this.setState({ pending_case_list: props.pending_case_list });
    }
    handleSubmit(e) {
        e.preventDefault();
        if (!this.state.query_date) {
            this.setState({ query_date_error: true });

        }
        else {
            this.setState({ query_date_error: false });
            const requestOptions = {
                'day': this.state.query_date.getDate().toString(),
                'month': (this.state.query_date.getMonth() + 1).toString(),
                'year': this.state.query_date.getFullYear().toString()
            };
            console.log(requestOptions);
            axios.post('/api/queryFreeSlot', requestOptions)
                .then(res => {
                    console.log(res.data);
                    this.setState({ free_slot: res.data.free_slot, val: "1" });
                })
                .catch(err => {
                    alert('Error in Server ' + err.response.status);
                    console.log(err.response);
                });
        }
    }

    handleChange(date) {
        this.setState({ query_date: date });
        if (date == null) {
            this.setState({ query_date_error: true });

        }
        else {
            this.setState({ query_date_error: false });
        }
    }
    render() {
        //Entry Adj
        if (this.state.val == "4") {
            return (

                <Router>
                    <div className="Registrar">
                        <div className="Registrar-header">
                            <h1>Give Adjournment Details for CIN:{this.state.selected_cin}</h1>
                            <AdjForm cin={this.state.selected_cin} goback={this.props.goback} />
                        </div>
                    </div>
                </Router>
            );
        }
        else if (this.state.val == "3") {
            //Choose Case
            return (
                <Router>
                    <div className="Registrar">
                        <div className="Registrar-header">
                            <AddCase getAddedCIN={(cin) => { this.setState({ selected_cin: cin }, () => this.handleAssignHearingDate()); this.setState({ val: "4" }); }}  goback={() => { this.setState({ val: "1" }) }} />
                        </div>
                    </div>
                </Router>
            );
        }
        else if (this.state.val == "2") {
            //When free slots have been chosen
            return (
                <Router>
                    <div className="Registrar">
                        <div className="Registrar-header">
                            <button
                                onClick={() => { this.setState({ val: "1" }) }}
                                style={{ marginLeft: "auto" }}
                                className="btn btn-primary "
                            >
                                Go Back
                            </button>
                            <button className="btn btn-primary " onClick={() => { this.setState({ val: "3" }) }}>Create New Case</button>
                            <h3>Select From Pending Cases</h3>
                            <ViewPendingCases handleselect={(props) => { this.setState({ selected_cin: props.data.cin }, () => this.handleAssignHearingDate()); this.setState({ val: "4" }); }} />
                        </div>
                    </div>
                </Router>
            );
        }
        else if (this.state.val == "1") {
            //Chose slot
            return (
                <Router>
                    <div className="Registrar">
                        <div className="Registrar-header">
                            {this.state.free_slot != null ? <DispSlots goback={this.goback} handleSelectSlot={this.handleSelectSlot} free_slot={this.state.free_slot} /> : null}
                        </div>
                    </div>
                </Router>
            );
        }
        else {
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
                                <h3>Query Free Slots</h3>
                                <div className="form-group">
                                    Enter Date: <DatePicker dateFormat="dd-MM-y" selected={this.state.query_date} onChange={this.handleChange} />
                                    {this.state.query_date_error ? <div style={{ color: "red" }}>Query Date cannot be Empty</div> : ""}
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
}