# PACE Documentation Contribution Template

## Document Metadata
* **Author**: [Your Name]
* **Date Created**: [YYYY-MM-DD]
* **Last Updated**: [YYYY-MM-DD]
* **Applicable Clusters**: [Select all that apply: Phoenix, ICE, Hive]

## [Title of Tool/Service/Process]

### Overview
[Provide 1-2 paragraphs explaining:
- What this tool/service is
- Its primary use cases
- Why it's relevant to PACE users at Georgia Tech]

### Prerequisites
- Required access/permissions:
  - [e.g., Active PACE account]
  - [Specific allocation requirements]
- Software dependencies:
  - [List required software]
  - [Version requirements]
- Storage requirements:
  - [Amount of space needed]
  - [Location requirements]
- Other prerequisites:
  - [Additional requirements]

### Step-by-Step Instructions

1. First Step
   ```bash
   # Example command with explanation
   module load software/1.2.3
   ```
   Expected output:
   ```
   [Example output text]
   ```

2. Second Step
   ```bash
   # Next command
   command --flag value
   ```

[Continue with numbered steps as needed]

### Configuration Details
1. Configuration File Setup
   ```yaml
   # Example configuration
   parameter1: value1
   parameter2: value2
   ```

2. Parameter Descriptions
   - `parameter1`: Description of first parameter
   - `parameter2`: Description of second parameter

### Troubleshooting

#### Common Issue 1
**Error Message:**
```
[Exact error message text]
```

**Resolution:**
1. First troubleshooting step
2. Second troubleshooting step

#### Common Issue 2
[Follow same format as above]

### Storage and Resource Considerations
- Disk Space Requirements:
  - Temporary storage: [amount]
  - Permanent storage: [amount]
- Memory Usage:
  - Minimum: [amount]
  - Recommended: [amount]
- CPU Requirements:
  - Minimum cores: [number]
  - Optimal performance: [number]
- Quota Impact:
  - [Description of how this affects PACE quotas]

### Directory Structure
```
project/
├── bin/
│   └── [executable files]
├── config/
│   └── [configuration files]
└── data/
    └── [data files]
```

### Additional Resources
- Internal PACE Documentation:
  - [Link to related PACE docs]
- External Resources:
  - [Link to software documentation]
  - [Link to relevant tutorials]

### Complete Working Example
```bash
# Full example demonstrating typical usage
module load required/modules
command --typical-flags typical-values
```

Expected workflow and output:
```
[Complete example output]
```

**NOTE**: Important information that users should know goes here.

**WARNING**: Critical warnings about potential issues go here.

### Version Information
- Software version documented: [version number]
- Last tested on PACE: [date]
- Compatible PACE environments: [list environments]
