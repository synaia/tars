/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { loadBundle } from "@web/core/assets";
import { registry } from "@web/core/registry";
import { formatFloat } from "@web/views/fields/formatters";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

import { Component, onWillStart, useEffect, useRef } from "@odoo/owl";

export class CustomProgressBarField extends Component {
    setup() {
        this.chart = null;
        this.canvasRef = useRef("canvas");

        onWillStart(async () => await loadBundle("web.chartjs_lib"));

        useEffect(() => {
            this.renderChart();
            return () => {
                if (this.chart) {
                    this.chart.destroy();
                }
            };
        });
    }

    get title() {
        return this.props.title || this.props.record.fields[this.props.name].string || "";
    }

    get formattedValue() {
        return formatFloat(this.props.record.data[this.props.name], {
            humanReadable: true,
            decimals: 1,
        });
    }

    renderChart() {
        const progressBarValue = this.props.record.data[this.props.name];
        const maxValue = parseFloat(this.props.maxValue); // Get max value from props
        const remainingValue = maxValue - progressBarValue;
        const labelValue = this.formattedValue;

        const config = {
            type: "doughnut",
            data: {
                datasets: [
                    {
                        data: [progressBarValue, remainingValue],
                        backgroundColor: [this.props.backgroundColor, "#dddddd"], // Use backgroundColor from props
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: "80%",
                plugins: {
                    title: {
                        display: true,
                        text: this.title,
                        padding: 0,
                    },
                    tooltip: {
                        enabled: false,
                    },
                    datalabels: {
                        display: true,
                        formatter: () => labelValue,
                        color: "#000",
                        font: {
                            size: 16,
                            weight: "bold",
                        },
                    },
                },
                layout: {
                    padding: 20,
                },
            },
        };

        this.chart = new Chart(this.canvasRef.el, config);
    }
}

CustomProgressBarField.template = "web.CustomProgressBarField";
CustomProgressBarField.props = {
    ...standardFieldProps,
    title: { type: String, optional: true },
    maxValue: { type: Number, optional: true }, // Add maxValue prop
    backgroundColor: { type: String, optional: true }, // Add backgroundColor prop
};

export const doughnutProgressField = {
    component: CustomProgressBarField,
    supportedOptions: [
        {
            label: _t("Title"),
            name: "title",
            type: "string",
        },
        {
            label: _t("Max Value"),
            name: "maxValue",
            type: "number",
        },
        {
            label: _t("Background Color"),
            name: "backgroundColor",
            type: "string",
        },
    ],
    extractProps: ({ options }) => ({
        title: options.title,
        maxValue: options.maxValue || 9, // Extract maxValue or use default 9
        backgroundColor: options.backgroundColor || "#1f77b4", // Extract backgroundColor or use default color
    }),
};

registry.category("fields").add("custom_progress_bar", doughnutProgressField);
