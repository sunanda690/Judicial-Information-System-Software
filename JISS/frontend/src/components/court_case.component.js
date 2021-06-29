import GridLayout from 'react-grid-layout';
import React, { Component } from "react";
import { AgGridColumn, AgGridReact } from 'ag-grid-react';

import 'ag-grid-community/dist/styles/ag-grid.css';
import 'ag-grid-community/dist/styles/ag-theme-balham-dark.css';

import Table from "./table.js";
import "./court-case.css";

export default class CourtCase extends Component {
  constructor(props) {
    super(props);
    //Details of the Court Case
    if(props.case_data==null)
    {
      this.state = {
        def_name: "",
        def_addr: "",
        pros_name: "",        
        crime_type: "",
        crime_date: "",
        crime_loc: "",
        arresting_off_name: "",
        date_arrest: "",
        CIN: "",
        date_hearing: "",
        latest_hearing_date: "",
        case_hearing_details: [{ date: "Date", reason: "Reason" }],
        name_pres_judge: "",
        start_date: "",
        expected_completion_of_trial: ""
      }
    }
    else
    {
      try {
        this.state = {
          def_name: props.case_data.def_name,
          def_addr: props.case_data.def_addr,
          pros_name: props.case_data.pros_name,          
          crime_type: props.case_data.crime_type,
          crime_date: props.case_data.crime_date,
          crime_loc: props.case_data.crime_loc,
          arresting_off_name: props.case_data.arresting_off_name,
          date_arrest: props.case_data.date_arrest,
          CIN: props.case_data.CIN,
          date_hearing: props.case_data.date_hearing,
          latest_hearing_date: props.case_data.latest_hearing_date,
          case_hearing_details: props.case_data.adj_details,
          name_pres_judge: props.case_data.name_pres_judge,
          start_date: props.case_data.start_date,
          expected_completion_of_trial: props.case_data.expected_completion_date
        };
        console.log('Adjourn Details : ',this.state.case_hearing_details);
        
      } catch (error) {
        console.log("Error in Getting Case Data");
        
      }
      
    }
    
  }
  render() {
    //fetch("/api/account").then(res => res.json()).then(res => { console.log(res); });
    // layout is an array of objects, see the demo for more complete usage
    const layout = [
      { i: '1', x: 0, y: 0, w: 5, h: 2, static: true },
      { i: '2', x: 10, y: 0, w: 5, h: 2, static: true },
      { i: '3', x: 2, y: 10, w: 10, h: 2, static: true }
    ];
    const columns = [{
      Header: 'Date',
      accessor: 'date'
    }, {
      Header: 'Reason',
      accessor: 'reason'
    }]
    console.log(columns.length);
    return (
      <div className="CourtCase">
        <GridLayout layout={layout} cols={12} rowHeight={30} width={1200}>
          <div key="1">
            <h1>Case : {this.state.CIN}</h1>
            <b>Defendent Name :</b> {this.state.def_name}
            <br />
            <b>Defendent Address :</b> {this.state.def_addr}
            <br /><br />
            <b>Prosecutor Name :</b> {this.state.pros_name}            
            <br /><br />
            <b>Hearing Date: </b>{this.state.date_hearing}
            <br />
            <b>Latest Hearing Date: </b>{this.state.latest_hearing_date}
          </div>
          <div key="2">
            <b>Crime Type :</b>  {this.state.crime_type}
            <br />
            <b>Crime Date :</b>  {this.state.crime_date}
            <br />
            <b>Crime Location : </b>{this.state.crime_loc}
            <br />
            <b>Name of Arresting Officer :</b>{this.state.arresting_off_name}
            <br />
            <b>Date of Arrest :</b> {this.state.date_arrest}<br />
            <b>Starting Date of Hearing: </b>{this.state.start_date}<br />
            <b>Expected Completion of Trial: </b>{this.state.expected_completion_of_trial}<br />
          </div>
          <div key="3">
            <h2>Summary of Hearings</h2>

            
            <div className="ag-theme-balham-dark" style={{ height: 300, width: 600 }}>                
                    <AgGridReact                       
                        rowData={this.state.case_hearing_details}>
                        <AgGridColumn field="date"></AgGridColumn>
                        <AgGridColumn field="reason"></AgGridColumn>
                    </AgGridReact>
              </div>

          </div>
        </GridLayout>
        <div style={{ display: "flex" }}>
          <button
            onClick={this.props.goback}
            style={{ marginLeft: "auto" }}
          >
            Go Back
        </button>
        </div>
        
      </div>
    )
  }
}