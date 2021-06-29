import GridLayout from 'react-grid-layout';
import React, { Component, useMemo, useState, useEffect } from "react";
import { AgGridColumn, AgGridReact } from 'ag-grid-react';

import 'ag-grid-community/dist/styles/ag-grid.css';
import 'ag-grid-community/dist/styles/ag-theme-balham-dark.css';
import './dispCIN.css';

export default class DispCIN extends Component {
    constructor(props) {
        super(props);
        console.log("DISP:: ",props);
        //Details of the Court Case
        if (props.cin_list == null) {
            //default values for testings 
            this.state = {
                cin_list_data: [{ cin: "1", crime_type: "Theft" }, { cin: "2", crime_type: "theft" }],
                selected_cin: ""
            }
            this.handleClick = this.handleClick.bind(this);
        }
        else {
            try {
                this.state = {
                    cin_list_data: props.cin_list,
                    selected_cin: ""
                };
                console.log('DISP CIN:: ',this.state.cin_list)

            } catch (error) {
                console.log("Error in Getting Case Data");
            }

        }

    }
    handleClick(e) {
        console.log(e.data.cin);
    }
    render() {
        return (
            <div className="DispCIN-header">
                <div className="ag-theme-balham-dark" style={{ height: 400, width: 600 }}>
                {console.log(this.state.cin_list_data)}
                    <AgGridReact                       
                        rowData={this.state.cin_list_data}>
                        <AgGridColumn onCellClicked={this.props.handleselect} field="cin"></AgGridColumn>
                        <AgGridColumn field="crime_type"></AgGridColumn>
                    </AgGridReact>
                </div>
                <button
                    onClick={this.props.goback}
                    style={{ marginLeft: "auto" }}
                >
                    Go Back
                </button>
            </div>
        );

    }
}