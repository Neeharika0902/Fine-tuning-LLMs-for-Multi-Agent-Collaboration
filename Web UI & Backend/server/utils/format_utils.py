"""
Formatting utilities for the multi-agent chatbot system
"""

def build_table_string(data, headers):
    """
    Build a well-formatted ASCII table string from data and headers
    
    Parameters:
    data (list): List of data rows
    headers (list): List of column headers
    
    Returns:
    str: Formatted ASCII table as a string
    """
    # Calculate column widths
    col_widths = [len(str(col)) for col in headers]
    for row in data:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    # Function to create a row line
    def make_row(row_data, sep="|"):
        return sep + sep.join(f" {str(cell).ljust(col_widths[i])} " for i, cell in enumerate(row_data)) + sep

    # Top border
    top_border = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"

    # Build table lines
    lines = [top_border]
    lines.append(make_row(headers))
    lines.append(top_border.replace("-", "="))
    for row in data:
        lines.append(make_row(row))
        lines.append(top_border)

    return "\n".join(lines)
