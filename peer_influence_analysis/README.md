# Peer Influence Analysis: Social Network Analysis System

## Overview
The Peer Influence Analysis module uses **social network analysis** to map and analyze student relationships, peer connections, and social influence patterns within educational settings. It creates visual network graphs showing how students are connected through shared classes and projects, enabling educators to understand peer dynamics and their impact on academic performance.

## 🎯 **What It Does**

### **Core Functionality:**
- **🕸️ Network Mapping**: Creates visual representations of student peer connections
- **👥 Relationship Analysis**: Identifies how students are connected through classes and projects
- **📊 Performance Correlation**: Color-codes students by academic performance levels
- **🔍 Influence Patterns**: Reveals potential peer influence and social learning opportunities

### **Key Features:**
- **Social Network Analysis**: Uses NetworkX library for graph theory and network visualization
- **Dynamic Group Generation**: Simulates project groups and peer connections
- **Performance Visualization**: Color-coded nodes based on academic achievement
- **Interactive Network Graphs**: Visual exploration of student relationships

## 🕸️ **Social Network Analysis Approach**

### **Network Structure:**
- **Nodes**: Individual students with attributes (name, performance level)
- **Edges**: Peer connections based on shared classes and project groups
- **Attributes**: Academic performance data attached to each student node
- **Layout**: Spring layout algorithm for optimal network visualization

### **Connection Synthesis:**
Since real peer relationship data isn't available, the system creates synthetic connections:

```python
# Group students by shared classes
for course_id, group in df_term_relations.groupby('course_id'):
    class_roster = list(group['student_id'].unique())
    
    # Create project groups of 3-4 students
    group_size = random.choice([3, 4])
    for i in range(0, len(class_roster), group_size):
        project_group = class_roster[i:i + group_size]
        
        # Connect all students within each project group
        for u, v in itertools.combinations(project_group, 2):
            edges.append((u, v))
```

### **Performance Categorization:**
Students are classified into three performance levels:
- **🔵 High-Performing**: Final scores ≥ 85 (skyblue nodes)
- **🟢 Average-Performing**: Final scores 70-84 (lightgreen nodes)
- **🔴 At-Risk**: Final scores < 70 (salmon nodes)

## 📊 **Sample Results & Analysis**

### **Current Network Analysis (Spring 2025):**
- **Total Students**: All students from student_master.csv
- **Peer Connections**: 1 synthesized connection (based on class groupings)
- **Performance Distribution**: Visual representation across the network
- **Network Visualization**: Interactive graph saved as `student_peer_network.png`

### **Network Insights:**
- **Connection Patterns**: Shows how students are grouped in classes and projects
- **Performance Clustering**: Reveals if high/low performers tend to group together
- **Social Learning Opportunities**: Identifies potential peer tutoring and study groups
- **Influence Pathways**: Maps how academic performance might spread through peer networks

## 🔍 **Analysis Process**

### **Step 1: Data Loading & Preparation**
- **Robust path detection** for data directory access
- **Multi-source integration**: Student, academic, and relational data
- **Data validation** and quality checks

### **Step 2: Peer Connection Synthesis**
- **Class-based grouping**: Students grouped by shared courses
- **Project group creation**: Random groups of 3-4 students
- **Edge generation**: Full connections within each project group
- **Network construction**: Building the graph structure

### **Step 3: Network Graph Construction**
- **Node creation**: All students added as network nodes
- **Attribute assignment**: Performance data attached to nodes
- **Edge addition**: Peer connections established
- **Graph optimization**: Layout algorithm applied

### **Step 4: Performance Integration**
- **Score categorization**: Students classified by performance level
- **Color mapping**: Visual distinction between performance categories
- **Attribute storage**: Performance data stored in node attributes

### **Step 5: Network Visualization**
- **Layout generation**: Spring layout for optimal node positioning
- **Color coding**: Performance-based node coloring
- **Legend creation**: Performance category explanations
- **Image saving**: Network graph saved to script directory

## 📁 **Data Requirements**

### **Required CSV Files:**
- **`student_master.csv`**: Student demographics and basic information
- **`academic_performance.csv`**: Course scores and performance data
- **`relational_social.csv`**: Student-course relationships and class enrollments

### **Expected Columns:**
- **Student Master**: `student_id`, `first_name`, `last_name`
- **Academic Performance**: `student_id`, `term`, `final_score`
- **Relational Social**: `student_id`, `term`, `course_id`

### **Data Quality Features:**
- **Handles missing data** gracefully
- **Automatic type conversion** for numerical fields
- **Robust error handling** for file access issues
- **Term-based filtering** for current academic period

## 🚀 **Usage**

### **Run the Complete Analysis:**
```bash
# From repository root
python "peer_influence_analysis\analyze_peer_network.py"

# From inside the module directory
python analyze_peer_network.py
```

### **Custom Analysis:**
```python
from peer_influence_analysis.analyze_peer_network import find_data_directory

# Use the path detection function in other scripts
data_path = find_data_directory()
```

## ⚙️ **Configuration**

### **Path Detection:**
Automatically detects data directory from multiple locations:
- `data/` (if running from root)
- `../data/` (if running from peer_influence_analysis subdirectory)
- `./data/` (if data is in current directory)

### **Network Parameters:**
- **Group Sizes**: Random selection between 3-4 students per project group
- **Layout Algorithm**: Spring layout with k=0.5 and 50 iterations
- **Node Sizing**: 1500 pixels for optimal visibility
- **Color Scheme**: Performance-based color coding system

### **Image Saving:**
All visualizations are automatically saved within the script's directory:
- `student_peer_network.png` - Complete peer network visualization

## 🎓 **Educational Applications**

### **For Teachers:**
- **Group Formation**: Identify optimal student groupings for projects
- **Peer Tutoring**: Match high performers with struggling students
- **Classroom Dynamics**: Understand social relationships and influence patterns
- **Collaborative Learning**: Design activities that leverage peer connections

### **For Counselors:**
- **Social Support**: Identify students who might benefit from peer mentoring
- **Isolation Detection**: Find students with limited social connections
- **Influence Mapping**: Understand how peer relationships affect behavior
- **Intervention Planning**: Design social support programs

### **For Administrators:**
- **Program Design**: Create peer mentoring and study group initiatives
- **Resource Allocation**: Target social support resources effectively
- **Policy Development**: Design policies that promote positive peer influence
- **Retention Strategies**: Leverage peer networks for student engagement

### **For Researchers:**
- **Social Network Analysis**: Study peer influence on academic outcomes
- **Performance Correlation**: Analyze relationship between social connections and grades
- **Longitudinal Studies**: Track how peer networks evolve over time
- **Intervention Research**: Measure effectiveness of peer-based programs

## 🔬 **Technical Details**

### **Requirements:**
- Python 3.7+
- pandas, networkx
- matplotlib
- Standard library modules (os, random, itertools)

### **Algorithm Details:**
- **Graph Theory**: NetworkX library for network analysis
- **Layout Algorithms**: Spring layout for optimal node positioning
- **Random Grouping**: Stochastic project group formation
- **Performance Mapping**: Categorical classification of academic achievement

### **Performance Considerations:**
- **Scalability**: Handles varying numbers of students and connections
- **Memory Efficiency**: Optimized graph construction and visualization
- **Randomization**: Reproducible results with controlled randomness
- **Error Handling**: Graceful degradation for missing or invalid data

## 📈 **Network Metrics & Analysis**

### **Key Network Measures:**
- **Degree Centrality**: Number of connections per student
- **Clustering Coefficient**: How tightly connected peer groups are
- **Network Density**: Overall connectivity of the student population
- **Performance Distribution**: Spread of academic achievement across the network

### **Influence Analysis:**
- **Peer Effects**: How student performance correlates with peer performance
- **Social Learning**: Opportunities for knowledge transfer between students
- **Support Networks**: Identification of potential mentoring relationships
- **Risk Factors**: Students who might be isolated or disconnected

## 🔮 **Future Enhancements**

### **Planned Features:**
- **Real-Time Updates**: Dynamic network updates as relationships change
- **Influence Scoring**: Quantitative measures of peer influence strength
- **Temporal Analysis**: Track network evolution across multiple terms
- **Predictive Modeling**: Forecast peer influence on academic outcomes
- **Interactive Dashboards**: Web-based network exploration tools
- **Mobile Integration**: Network analysis on mobile devices

### **Advanced Analytics:**
- **Community Detection**: Identify natural student groups and cliques
- **Influence Propagation**: Model how behaviors spread through networks
- **Centrality Analysis**: Identify key influencers and connectors
- **Network Resilience**: Analyze robustness of peer support systems

## 🛡️ **Ethical Considerations**

### **Data Privacy:**
- **Student Confidentiality**: Network data must be handled with care
- **Limited Access**: Network visualizations for authorized personnel only
- **Anonymization Options**: Ability to remove identifying information
- **Consent Management**: Respect student privacy preferences

### **Interpretation Guidelines:**
- **Correlation ≠ Causation**: Network connections don't guarantee influence
- **Individual Agency**: Students make their own academic choices
- **Support Focus**: Use insights to provide assistance, not to label
- **Professional Judgment**: Combine network analysis with human expertise
- **Positive Framing**: Emphasize opportunities for peer support and collaboration

## 📚 **Related Modules**

This module works alongside other Snowball analysis modules:
- **Teacher Effectiveness Analysis**: Examines teaching impact on peer dynamics
- **Personalized Learning Pathways**: Creates individual strategies considering peer context
- **Behavioral Analysis**: Monitors how peer relationships affect student behavior
- **Dropout Risk Detection**: Identifies social isolation as a risk factor

## 🔧 **Troubleshooting**

### **Common Issues:**
- **"Data directory not found"**: Ensure `data/` folder exists at repository root
- **"No peer connections synthesized"**: Check if relational_social.csv has class data
- **"Network too sparse"**: Adjust group size parameters for more connections
- **"Visualization issues"**: Ensure matplotlib is properly installed

### **Solutions:**
- Verify CSV file structure matches expected columns
- Check for sufficient class enrollment data
- Adjust group size parameters for desired network density
- Update matplotlib and networkx installations if needed

## 📊 **Success Metrics**

### **Network Effectiveness:**
- **Connection Density**: Percentage of possible peer connections realized
- **Performance Balance**: Distribution of performance levels across groups
- **Social Integration**: Reduction in isolated students
- **Peer Support**: Increased collaborative learning opportunities

### **Educational Outcomes:**
- **Academic Performance**: Improved grades through peer influence
- **Student Engagement**: Higher participation in collaborative activities
- **Social Skills**: Development of teamwork and communication abilities
- **Retention Rates**: Better student persistence through peer support

## 🎨 **Visualization Features**

### **Network Graph Elements:**
- **Node Colors**: Performance-based color coding (skyblue, lightgreen, salmon)
- **Node Labels**: Student names for easy identification
- **Edge Styling**: Gray connections showing peer relationships
- **Layout Optimization**: Spring algorithm for clear network structure
- **Legend**: Performance category explanations
- **High Resolution**: 18x18 inch output for detailed analysis

### **Interactive Features:**
- **Zoom Capability**: Explore network details at different scales
- **Node Identification**: Clear labeling of all student nodes
- **Performance Mapping**: Visual correlation between connections and grades
- **Export Options**: High-quality PNG output for reports and presentations

---

**Note**: This module is designed to work with the Snowball educational data analysis project and provides a foundation for understanding peer dynamics and social learning opportunities. All network analysis should be interpreted with care and used to promote positive peer relationships and collaborative learning rather than to make assumptions about individual student capabilities. 