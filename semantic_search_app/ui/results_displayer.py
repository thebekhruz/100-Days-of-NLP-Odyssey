import streamlit as st


class ResultsDisplayer:
    def __init__(self, container, results, output_type):
        self.results = results
        self.output_type = output_type
        self.container = container
        self.display_results(container, results, output_type)

    def display_results(self, container, results, output_type):
        if output_type == "Json":
            self.display_json(container, results)
        elif output_type == "Table":
            self.prepare_table_data(container, results)
        elif output_type == "Graph":
            pass
        else:
            st.error("Invalid output type selected.")

    def prepare_table_data(self, container, results):
        """Prepares data for tabular display and displays it, including beautifully formatted relationship properties."""
        table_data = []
        for record in results:
            subject = record["n"]
            relationship = record.get("r")
            target = record.get("m")

            row = {
                "Subject Label": ", ".join(subject.labels),
                **subject._properties,
            }

            # Format and include relationship properties if present
            if relationship:
                ne_properties = self.format_relationship_properties(relationship)
                row.update(ne_properties)

            # Include target node properties and labels if present
            if target:
                if target.labels == "wiki_ID":
                    # if it contains wiki_id format the target name to include a link to that wiki_id
                    row["Target Labels"] = f"[{target.labels}](https://en.wikipedia.org/wiki/{target.labels})"
                    # If not do nothing
                else:
                    # Make sure to not output the wiki_id as a label
                    row["Target Labels"] = ", ".join(target.labels)
                row.update(
                    {
                        f"Target_{key}": value
                        for key, value in target._properties.items()
                    }
                )

            table_data.append(row)

        container.table(table_data)

    def format_relationship_properties(self, relationship):
        """Formats named entity properties from the relationship for display."""
        formatted_properties = {}
        # Check for each property and format
        if (
            "ne_start" in relationship._properties
            and "ne_end" in relationship._properties
        ):
            formatted_properties["Named Entity Position"] = (
                f"{relationship._properties['ne_start']}-{relationship._properties['ne_end']}"
            )
        if "ne_type" in relationship._properties:
            formatted_properties["Named Entity Type"] = relationship._properties[
                "ne_type"
            ]

        return formatted_properties

    def display_json(self, container, results):
        """Prepares and displays data in JSON format."""
        json_data = []
        for record in results:
            subject = record["n"]
            relationship = record.get("r")
            target = record.get("m")

            # Create a dictionary for each record, incorporating subject, relationship, and target data
            record_data = {
                "Subject": {
                    "Labels": list(subject.labels),
                    "Properties": subject._properties,
                }
            }

            if relationship:
                # Format and include relationship properties
                ne_properties = self.format_relationship_properties(relationship)
                record_data["Relationship"] = {
                    "Properties": relationship._properties,
                    "Formatted Properties": ne_properties,
                }

            if target:
                # Include target node properties and labels
                record_data["Target"] = {
                    "Labels": list(target.labels),
                    "Properties": target._properties,
                }

            json_data.append(record_data)

        with container:
            st.json(json_data)



    # def prepare_table_data(self, container, results):

    #     """Generates and displays data in an HTML table, including beautifully formatted relationship properties with optional Wikipedia links."""
    #     # Start of the HTML table
    #     html_table = "<table style='border-collapse: collapse;'>"
    #     html_table += "<tr style='background-color: #f2f2f2;'>"
    #     html_table += "<th style='border: 1px solid #dddddd; text-align: left; padding: 8px;'>Subject Label</th>"
    #     html_table += "<th style='border: 1px solid #dddddd; text-align: left; padding: 8px;'>Properties</th>"
    #     html_table += "<th style='border: 1px solid #dddddd; text-align: left; padding: 8px;'>Target Labels</th>"
    #     html_table += "<th style='border: 1px solid #dddddd; text-align: left; padding: 8px;'>Wiki ID</th>"
    #     html_table += "</tr>"

    #     for record in results:
    #         subject = record["n"]
    #         relationship = record.get("r")
    #         target = record.get("m")

    #         subject_label = ", ".join(subject.labels)
    #         properties = ", ".join([f"{k}: {v}" for k, v in subject._properties.items()])

    #         # Initialize Target Labels and Wiki ID columns
    #         target_labels = "N/A"
    #         wiki_id = "N/A"

    #         # Include target node properties and labels if present
    #         if target:
    #             target_labels = ", ".join(target.labels)
    #             # Update the table with target properties
    #             target_properties = ", ".join([f"{key}: {value}" for key, value in target._properties.items()])

    #             # Check for wiki_ID and format the target name to include a link to the Wikipedia page
    #             if 'wiki_ID' in target._properties:
    #                 wiki_id = f"<a href='https://en.wikipedia.org/wiki/{target._properties['wiki_ID']}'>{target._properties['wiki_ID']}</a>"

    #         # Add row to the HTML table
    #         html_table += "<tr>"
    #         html_table += f"<td style='border: 1px solid #dddddd; text-align: left; padding: 8px;'>{subject_label}</td>"
    #         html_table += f"<td style='border: 1px solid #dddddd; text-align: left; padding: 8px;'>{properties}</td>"
    #         html_table += f"<td style='border: 1px solid #dddddd; text-align: left; padding: 8px;'>{target_labels}</td>"
    #         html_table += f"<td style='border: 1px solid #dddddd; text-align: left; padding: 8px;'>{wiki_id}</td>"
    #         html_table += "</tr>"

    #     # Close the HTML table
    #     html_table += "</table>"

    #     # Display the HTML table in Streamlit or any other HTML-supporting container
    #     # For Streamlit, use: st.markdown(html_table, unsafe_allow_html=True)
    #     # If you're not using Streamlit, you'll need to adapt this line to your specific environment
    #     container.markdown(html_table, unsafe_allow_html=True)

