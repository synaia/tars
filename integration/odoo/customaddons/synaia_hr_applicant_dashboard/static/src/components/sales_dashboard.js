/** @odoo-module */

import { registry } from "@web/core/registry"
import { KpiCard } from "./kpi_card"
import { ChartRenderer } from "./chart_renderer"
const { Component, onWillStart, useRef, onMounted } = owl

export class ApplicantDashboard extends Component {
    setup(){

    }
}

ApplicantDashboard.template = "synaia.ApplicantDashboard"
ApplicantDashboard.components = { KpiCard, ChartRenderer }

registry.category("actions").add("synaia.appl_dashboard", ApplicantDashboard)