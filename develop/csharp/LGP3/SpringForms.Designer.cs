/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *\
     ___________________________
    |                           |___________________
   O|  Gas Spring calculator.   |___________________O
    |___________________________|


   Developed on Visual Studio Express 2012.
   And Linux, Vim, Mono and Wine. Deployed to Windows 7+.
   Depends on .NET-4

   Copyright:               Lesjofors AB
   Original author:         Niklas Wikstrom, FS Dynamics AB
   Author contact:          niklas.wikstrom@gmail.com
   Year of first release:   2013
   Version:                 1.0-beta

\* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */


namespace HatchTest
{
    partial class SpringForms
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.Windows.Forms.DataVisualization.Charting.ChartArea chartArea1 = new System.Windows.Forms.DataVisualization.Charting.ChartArea();
            System.Windows.Forms.DataVisualization.Charting.Series series1 = new System.Windows.Forms.DataVisualization.Charting.Series();
            System.Windows.Forms.DataVisualization.Charting.Title title1 = new System.Windows.Forms.DataVisualization.Charting.Title();
            this.hatchBox = new System.Windows.Forms.PictureBox();
            this.inputSubmit = new System.Windows.Forms.Button();
            this.SpringBox = new System.Windows.Forms.ListBox();
            this.startAngleLabel = new System.Windows.Forms.Label();
            this.openingAngleInput = new System.Windows.Forms.NumericUpDown();
            this.startAngleInput = new System.Windows.Forms.NumericUpDown();
            this.angleSlider = new System.Windows.Forms.TrackBar();
            this.stopAngleLabel = new System.Windows.Forms.Label();
            this.currentAngleLabel = new System.Windows.Forms.Label();
            this.NoSpringsText = new System.Windows.Forms.Label();
            this.NoSpringsLabel = new System.Windows.Forms.Label();
            this.endFittingTubeBox = new System.Windows.Forms.ComboBox();
            this.GeometricInputGroup = new System.Windows.Forms.GroupBox();
            this.temperatureGroupBox = new System.Windows.Forms.GroupBox();
            this.temperatureInput = new System.Windows.Forms.NumericUpDown();
            this.temperatureLabel = new System.Windows.Forms.Label();
            this.ResetButton = new System.Windows.Forms.Button();
            this.SpringInputGroupBox = new System.Windows.Forms.GroupBox();
            this.threadRadioWeld = new System.Windows.Forms.RadioButton();
            this.threadRadioAll = new System.Windows.Forms.RadioButton();
            this.endFittingRodBox = new System.Windows.Forms.ComboBox();
            this.threadRadioM8 = new System.Windows.Forms.RadioButton();
            this.threadRadioM6 = new System.Windows.Forms.RadioButton();
            this.nbrOfSpringsInput = new System.Windows.Forms.NumericUpDown();
            this.lidOffsetInput = new System.Windows.Forms.NumericUpDown();
            this.springOriginYInput = new System.Windows.Forms.NumericUpDown();
            this.lidConnectPosInput = new System.Windows.Forms.NumericUpDown();
            this.springOriginXInput = new System.Windows.Forms.NumericUpDown();
            this.endFittingRodLabel = new System.Windows.Forms.Label();
            this.endFittingTubeLabel = new System.Windows.Forms.Label();
            this.label8 = new System.Windows.Forms.Label();
            this.lidConnectPosLabel = new System.Windows.Forms.Label();
            this.label11 = new System.Windows.Forms.Label();
            this.lidOffsetLabel = new System.Windows.Forms.Label();
            this.springOriginXLabel = new System.Windows.Forms.Label();
            this.springOriginYLabel = new System.Windows.Forms.Label();
            this.label9 = new System.Windows.Forms.Label();
            this.nbrOfSpringsLabel = new System.Windows.Forms.Label();
            this.LidInputGroupBox = new System.Windows.Forms.GroupBox();
            this.weightInput = new System.Windows.Forms.NumericUpDown();
            this.cogInput = new System.Windows.Forms.NumericUpDown();
            this.lidLengthInput = new System.Windows.Forms.NumericUpDown();
            this.lidLengthLabel = new System.Windows.Forms.Label();
            this.cogLabel = new System.Windows.Forms.Label();
            this.weightLabel = new System.Windows.Forms.Label();
            this.statusStripBottom = new System.Windows.Forms.StatusStrip();
            this.toolStripStatusLabel1 = new System.Windows.Forms.ToolStripStatusLabel();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.minExtLenTextBox = new System.Windows.Forms.TextBox();
            this.minStrokeTextBox = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.springSelectionGroupBox = new System.Windows.Forms.GroupBox();
            this.selectedSpringGroupBox = new System.Windows.Forms.GroupBox();
            this.selectedFrictionTextBox = new System.Windows.Forms.TextBox();
            this.selectedFrictionLabel = new System.Windows.Forms.Label();
            this.selectedPartNoTextBox = new System.Windows.Forms.TextBox();
            this.selectedPartNoLabel = new System.Windows.Forms.Label();
            this.selectedForceTextBox = new System.Windows.Forms.TextBox();
            this.selectedForceLabel = new System.Windows.Forms.Label();
            this.selectedStrokeTextBox = new System.Windows.Forms.TextBox();
            this.label10 = new System.Windows.Forms.Label();
            this.lengthWithEndsTextBox = new System.Windows.Forms.TextBox();
            this.withEndsLengthLabel = new System.Windows.Forms.Label();
            this.selectedLengthTextBox = new System.Windows.Forms.TextBox();
            this.selectedLengthLabel = new System.Windows.Forms.Label();
            this.selectedTypeTextBox = new System.Windows.Forms.TextBox();
            this.selectedTypeLabel = new System.Windows.Forms.Label();
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.toolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.restoreLastToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.openToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.saveToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.toolStripSeparator1 = new System.Windows.Forms.ToolStripSeparator();
            this.printToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.exitToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.editToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.optionsMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.designerMailLabel = new System.Windows.Forms.Label();
            this.designerTelLabel = new System.Windows.Forms.Label();
            this.designerNameLabel = new System.Windows.Forms.Label();
            this.customerBox = new System.Windows.Forms.GroupBox();
            this.label58 = new System.Windows.Forms.Label();
            this.label57 = new System.Windows.Forms.Label();
            this.label56 = new System.Windows.Forms.Label();
            this.label55 = new System.Windows.Forms.Label();
            this.customerMailTextBox = new System.Windows.Forms.TextBox();
            this.customerProjectTextBox = new System.Windows.Forms.TextBox();
            this.customerNameTextBox = new System.Windows.Forms.TextBox();
            this.customerCompanyTextBox = new System.Windows.Forms.TextBox();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.sliderLimitLabel = new System.Windows.Forms.Label();
            this.sliderRadioLimitOff = new System.Windows.Forms.RadioButton();
            this.sliderRadioLimitInput = new System.Windows.Forms.RadioButton();
            this.sliderRadioLimitSpring = new System.Windows.Forms.RadioButton();
            this.chart1 = new System.Windows.Forms.DataVisualization.Charting.Chart();
            this.designerBox = new System.Windows.Forms.GroupBox();
            this.designerMailTextBox = new System.Windows.Forms.TextBox();
            this.designerTelTextBox = new System.Windows.Forms.TextBox();
            this.designerNameTextBox = new System.Windows.Forms.TextBox();
            this.selfOpeningAngleLabel = new System.Windows.Forms.Label();
            this.selfOpeningAngleTextBox = new System.Windows.Forms.TextBox();
            this.toolTip1 = new System.Windows.Forms.ToolTip(this.components);
            this.groupBox3 = new System.Windows.Forms.GroupBox();
            this.label4 = new System.Windows.Forms.Label();
            this.overshootTextBox = new System.Windows.Forms.TextBox();
            this.maxOpeningAngleLabel = new System.Windows.Forms.Label();
            this.maxOpeningAngleTextBox = new System.Windows.Forms.TextBox();
            this.endsBox = new System.Windows.Forms.GroupBox();
            this.endFittings2Label = new System.Windows.Forms.Label();
            this.endFittings1Label = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.hatchBox)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.openingAngleInput)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.startAngleInput)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.angleSlider)).BeginInit();
            this.GeometricInputGroup.SuspendLayout();
            this.temperatureGroupBox.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.temperatureInput)).BeginInit();
            this.SpringInputGroupBox.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.nbrOfSpringsInput)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.lidOffsetInput)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.springOriginYInput)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.lidConnectPosInput)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.springOriginXInput)).BeginInit();
            this.LidInputGroupBox.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.weightInput)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.cogInput)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.lidLengthInput)).BeginInit();
            this.statusStripBottom.SuspendLayout();
            this.groupBox1.SuspendLayout();
            this.springSelectionGroupBox.SuspendLayout();
            this.selectedSpringGroupBox.SuspendLayout();
            this.menuStrip1.SuspendLayout();
            this.customerBox.SuspendLayout();
            this.groupBox2.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.chart1)).BeginInit();
            this.designerBox.SuspendLayout();
            this.groupBox3.SuspendLayout();
            this.endsBox.SuspendLayout();
            this.SuspendLayout();
            // 
            // hatchBox
            // 
            this.hatchBox.BackColor = System.Drawing.SystemColors.ButtonHighlight;
            this.hatchBox.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.hatchBox.Location = new System.Drawing.Point(210, 31);
            this.hatchBox.Name = "hatchBox";
            this.hatchBox.Size = new System.Drawing.Size(400, 380);
            this.hatchBox.TabIndex = 1;
            this.hatchBox.TabStop = false;
            // 
            // inputSubmit
            // 
            this.inputSubmit.Location = new System.Drawing.Point(120, 580);
            this.inputSubmit.Name = "inputSubmit";
            this.inputSubmit.Size = new System.Drawing.Size(75, 23);
            this.inputSubmit.TabIndex = 4;
            this.inputSubmit.Text = "Submit";
            this.inputSubmit.UseVisualStyleBackColor = true;
            this.inputSubmit.Click += new System.EventHandler(this.inputDataSubmitted);
            // 
            // SpringBox
            // 
            this.SpringBox.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.SpringBox.FormattingEnabled = true;
            this.SpringBox.Location = new System.Drawing.Point(6, 16);
            this.SpringBox.Name = "SpringBox";
            this.SpringBox.Size = new System.Drawing.Size(207, 184);
            this.SpringBox.TabIndex = 6;
            this.SpringBox.SelectedIndexChanged += new System.EventHandler(this.springListSelect);
            // 
            // startAngleLabel
            // 
            this.startAngleLabel.AutoSize = true;
            this.startAngleLabel.Location = new System.Drawing.Point(6, 96);
            this.startAngleLabel.Name = "startAngleLabel";
            this.startAngleLabel.Size = new System.Drawing.Size(58, 13);
            this.startAngleLabel.TabIndex = 7;
            this.startAngleLabel.Text = "Start angle";
            // 
            // openingAngleInput
            // 
            this.openingAngleInput.Increment = new decimal(new int[] {
            5,
            0,
            0,
            0});
            this.openingAngleInput.Location = new System.Drawing.Point(83, 120);
            this.openingAngleInput.Maximum = new decimal(new int[] {
            180,
            0,
            0,
            0});
            this.openingAngleInput.Minimum = new decimal(new int[] {
            180,
            0,
            0,
            -2147483648});
            this.openingAngleInput.Name = "openingAngleInput";
            this.openingAngleInput.Size = new System.Drawing.Size(99, 20);
            this.openingAngleInput.TabIndex = 4;
            this.openingAngleInput.ValueChanged += new System.EventHandler(this.inputField_ValueChanged);
            // 
            // startAngleInput
            // 
            this.startAngleInput.Increment = new decimal(new int[] {
            5,
            0,
            0,
            0});
            this.startAngleInput.Location = new System.Drawing.Point(83, 94);
            this.startAngleInput.Maximum = new decimal(new int[] {
            180,
            0,
            0,
            0});
            this.startAngleInput.Minimum = new decimal(new int[] {
            180,
            0,
            0,
            -2147483648});
            this.startAngleInput.Name = "startAngleInput";
            this.startAngleInput.Size = new System.Drawing.Size(99, 20);
            this.startAngleInput.TabIndex = 3;
            this.startAngleInput.ValueChanged += new System.EventHandler(this.inputField_ValueChanged);
            // 
            // angleSlider
            // 
            this.angleSlider.Location = new System.Drawing.Point(5, 14);
            this.angleSlider.Maximum = 180;
            this.angleSlider.Minimum = -180;
            this.angleSlider.Name = "angleSlider";
            this.angleSlider.Size = new System.Drawing.Size(389, 45);
            this.angleSlider.TabIndex = 12;
            this.angleSlider.ValueChanged += new System.EventHandler(this.slideAngle);
            // 
            // stopAngleLabel
            // 
            this.stopAngleLabel.AutoSize = true;
            this.stopAngleLabel.Location = new System.Drawing.Point(6, 122);
            this.stopAngleLabel.Name = "stopAngleLabel";
            this.stopAngleLabel.Size = new System.Drawing.Size(76, 13);
            this.stopAngleLabel.TabIndex = 13;
            this.stopAngleLabel.Text = "Opening angle";
            // 
            // currentAngleLabel
            // 
            this.currentAngleLabel.AutoSize = true;
            this.currentAngleLabel.Location = new System.Drawing.Point(360, 45);
            this.currentAngleLabel.Name = "currentAngleLabel";
            this.currentAngleLabel.Size = new System.Drawing.Size(19, 13);
            this.currentAngleLabel.TabIndex = 14;
            this.currentAngleLabel.Text = "----";
            // 
            // NoSpringsText
            // 
            this.NoSpringsText.AutoSize = true;
            this.NoSpringsText.Location = new System.Drawing.Point(147, 203);
            this.NoSpringsText.Name = "NoSpringsText";
            this.NoSpringsText.Size = new System.Drawing.Size(24, 13);
            this.NoSpringsText.TabIndex = 15;
            this.NoSpringsText.Text = "n/a";
            // 
            // NoSpringsLabel
            // 
            this.NoSpringsLabel.AutoSize = true;
            this.NoSpringsLabel.Location = new System.Drawing.Point(3, 203);
            this.NoSpringsLabel.Name = "NoSpringsLabel";
            this.NoSpringsLabel.Size = new System.Drawing.Size(146, 13);
            this.NoSpringsLabel.TabIndex = 16;
            this.NoSpringsLabel.Text = "Number of compatible springs";
            // 
            // endFittingTubeBox
            // 
            this.endFittingTubeBox.FormattingEnabled = true;
            this.endFittingTubeBox.Location = new System.Drawing.Point(9, 252);
            this.endFittingTubeBox.Name = "endFittingTubeBox";
            this.endFittingTubeBox.Size = new System.Drawing.Size(173, 21);
            this.endFittingTubeBox.TabIndex = 21;
            this.endFittingTubeBox.Text = "Welded";
            this.endFittingTubeBox.SelectedIndexChanged += new System.EventHandler(this.endFittingsSelect);
            // 
            // GeometricInputGroup
            // 
            this.GeometricInputGroup.Controls.Add(this.temperatureGroupBox);
            this.GeometricInputGroup.Controls.Add(this.ResetButton);
            this.GeometricInputGroup.Controls.Add(this.SpringInputGroupBox);
            this.GeometricInputGroup.Controls.Add(this.LidInputGroupBox);
            this.GeometricInputGroup.Controls.Add(this.inputSubmit);
            this.GeometricInputGroup.Location = new System.Drawing.Point(3, 26);
            this.GeometricInputGroup.Name = "GeometricInputGroup";
            this.GeometricInputGroup.Size = new System.Drawing.Size(201, 613);
            this.GeometricInputGroup.TabIndex = 22;
            this.GeometricInputGroup.TabStop = false;
            this.GeometricInputGroup.Text = "Define in [mm], [kg], [deg]";
            // 
            // temperatureGroupBox
            // 
            this.temperatureGroupBox.Controls.Add(this.temperatureInput);
            this.temperatureGroupBox.Controls.Add(this.temperatureLabel);
            this.temperatureGroupBox.Location = new System.Drawing.Point(6, 517);
            this.temperatureGroupBox.Name = "temperatureGroupBox";
            this.temperatureGroupBox.Size = new System.Drawing.Size(188, 55);
            this.temperatureGroupBox.TabIndex = 6;
            this.temperatureGroupBox.TabStop = false;
            this.temperatureGroupBox.Text = "Other";
            // 
            // temperatureInput
            // 
            this.temperatureInput.Increment = new decimal(new int[] {
            10,
            0,
            0,
            0});
            this.temperatureInput.Location = new System.Drawing.Point(114, 20);
            this.temperatureInput.Minimum = new decimal(new int[] {
            50,
            0,
            0,
            -2147483648});
            this.temperatureInput.Name = "temperatureInput";
            this.temperatureInput.Size = new System.Drawing.Size(68, 20);
            this.temperatureInput.TabIndex = 6;
            this.temperatureInput.ValueChanged += new System.EventHandler(this.inputField_ValueChanged);
            // 
            // temperatureLabel
            // 
            this.temperatureLabel.AutoSize = true;
            this.temperatureLabel.Location = new System.Drawing.Point(6, 22);
            this.temperatureLabel.Name = "temperatureLabel";
            this.temperatureLabel.Size = new System.Drawing.Size(67, 13);
            this.temperatureLabel.TabIndex = 7;
            this.temperatureLabel.Text = "Temperature";
            // 
            // ResetButton
            // 
            this.ResetButton.Location = new System.Drawing.Point(6, 579);
            this.ResetButton.Name = "ResetButton";
            this.ResetButton.Size = new System.Drawing.Size(75, 23);
            this.ResetButton.TabIndex = 5;
            this.ResetButton.Text = "Reset";
            this.ResetButton.UseVisualStyleBackColor = true;
            this.ResetButton.Click += new System.EventHandler(this.ResetButton_Click);
            // 
            // SpringInputGroupBox
            // 
            this.SpringInputGroupBox.Controls.Add(this.threadRadioWeld);
            this.SpringInputGroupBox.Controls.Add(this.threadRadioAll);
            this.SpringInputGroupBox.Controls.Add(this.endFittingRodBox);
            this.SpringInputGroupBox.Controls.Add(this.endFittingTubeBox);
            this.SpringInputGroupBox.Controls.Add(this.threadRadioM8);
            this.SpringInputGroupBox.Controls.Add(this.threadRadioM6);
            this.SpringInputGroupBox.Controls.Add(this.nbrOfSpringsInput);
            this.SpringInputGroupBox.Controls.Add(this.lidOffsetInput);
            this.SpringInputGroupBox.Controls.Add(this.springOriginYInput);
            this.SpringInputGroupBox.Controls.Add(this.lidConnectPosInput);
            this.SpringInputGroupBox.Controls.Add(this.springOriginXInput);
            this.SpringInputGroupBox.Controls.Add(this.endFittingRodLabel);
            this.SpringInputGroupBox.Controls.Add(this.endFittingTubeLabel);
            this.SpringInputGroupBox.Controls.Add(this.label8);
            this.SpringInputGroupBox.Controls.Add(this.lidConnectPosLabel);
            this.SpringInputGroupBox.Controls.Add(this.label11);
            this.SpringInputGroupBox.Controls.Add(this.lidOffsetLabel);
            this.SpringInputGroupBox.Controls.Add(this.springOriginXLabel);
            this.SpringInputGroupBox.Controls.Add(this.springOriginYLabel);
            this.SpringInputGroupBox.Controls.Add(this.label9);
            this.SpringInputGroupBox.Controls.Add(this.nbrOfSpringsLabel);
            this.SpringInputGroupBox.Location = new System.Drawing.Point(6, 191);
            this.SpringInputGroupBox.Name = "SpringInputGroupBox";
            this.SpringInputGroupBox.Size = new System.Drawing.Size(188, 320);
            this.SpringInputGroupBox.TabIndex = 0;
            this.SpringInputGroupBox.TabStop = false;
            this.SpringInputGroupBox.Text = "Spring";
            // 
            // threadRadioWeld
            // 
            this.threadRadioWeld.AutoSize = true;
            this.threadRadioWeld.Location = new System.Drawing.Point(9, 216);
            this.threadRadioWeld.Name = "threadRadioWeld";
            this.threadRadioWeld.Size = new System.Drawing.Size(50, 17);
            this.threadRadioWeld.TabIndex = 22;
            this.threadRadioWeld.TabStop = true;
            this.threadRadioWeld.Text = "Weld";
            this.threadRadioWeld.UseVisualStyleBackColor = true;
            // 
            // threadRadioAll
            // 
            this.threadRadioAll.AutoSize = true;
            this.threadRadioAll.Location = new System.Drawing.Point(148, 216);
            this.threadRadioAll.Name = "threadRadioAll";
            this.threadRadioAll.Size = new System.Drawing.Size(36, 17);
            this.threadRadioAll.TabIndex = 8;
            this.threadRadioAll.TabStop = true;
            this.threadRadioAll.Text = "All";
            this.threadRadioAll.UseVisualStyleBackColor = true;
            this.threadRadioAll.CheckedChanged += new System.EventHandler(this.threadSelect);
            // 
            // endFittingRodBox
            // 
            this.endFittingRodBox.FormattingEnabled = true;
            this.endFittingRodBox.Location = new System.Drawing.Point(9, 292);
            this.endFittingRodBox.Name = "endFittingRodBox";
            this.endFittingRodBox.Size = new System.Drawing.Size(173, 21);
            this.endFittingRodBox.TabIndex = 21;
            this.endFittingRodBox.Text = "Welded";
            this.endFittingRodBox.SelectedIndexChanged += new System.EventHandler(this.endFittingsSelect);
            // 
            // threadRadioM8
            // 
            this.threadRadioM8.AutoSize = true;
            this.threadRadioM8.Location = new System.Drawing.Point(105, 216);
            this.threadRadioM8.Name = "threadRadioM8";
            this.threadRadioM8.Size = new System.Drawing.Size(40, 17);
            this.threadRadioM8.TabIndex = 8;
            this.threadRadioM8.TabStop = true;
            this.threadRadioM8.Text = "M8";
            this.threadRadioM8.UseVisualStyleBackColor = true;
            this.threadRadioM8.CheckedChanged += new System.EventHandler(this.threadSelect);
            // 
            // threadRadioM6
            // 
            this.threadRadioM6.AutoSize = true;
            this.threadRadioM6.Location = new System.Drawing.Point(61, 216);
            this.threadRadioM6.Name = "threadRadioM6";
            this.threadRadioM6.Size = new System.Drawing.Size(40, 17);
            this.threadRadioM6.TabIndex = 8;
            this.threadRadioM6.TabStop = true;
            this.threadRadioM6.Text = "M6";
            this.threadRadioM6.UseVisualStyleBackColor = true;
            this.threadRadioM6.CheckedChanged += new System.EventHandler(this.threadSelect);
            // 
            // nbrOfSpringsInput
            // 
            this.nbrOfSpringsInput.Location = new System.Drawing.Point(83, 161);
            this.nbrOfSpringsInput.Maximum = new decimal(new int[] {
            10,
            0,
            0,
            0});
            this.nbrOfSpringsInput.Minimum = new decimal(new int[] {
            1,
            0,
            0,
            0});
            this.nbrOfSpringsInput.Name = "nbrOfSpringsInput";
            this.nbrOfSpringsInput.Size = new System.Drawing.Size(99, 20);
            this.nbrOfSpringsInput.TabIndex = 9;
            this.nbrOfSpringsInput.Value = new decimal(new int[] {
            1,
            0,
            0,
            0});
            this.nbrOfSpringsInput.ValueChanged += new System.EventHandler(this.inputField_ValueChanged);
            // 
            // lidOffsetInput
            // 
            this.lidOffsetInput.Increment = new decimal(new int[] {
            5,
            0,
            0,
            0});
            this.lidOffsetInput.Location = new System.Drawing.Point(83, 134);
            this.lidOffsetInput.Maximum = new decimal(new int[] {
            5000,
            0,
            0,
            0});
            this.lidOffsetInput.Minimum = new decimal(new int[] {
            1000,
            0,
            0,
            -2147483648});
            this.lidOffsetInput.Name = "lidOffsetInput";
            this.lidOffsetInput.Size = new System.Drawing.Size(99, 20);
            this.lidOffsetInput.TabIndex = 8;
            this.lidOffsetInput.ValueChanged += new System.EventHandler(this.inputField_ValueChanged);
            // 
            // springOriginYInput
            // 
            this.springOriginYInput.Increment = new decimal(new int[] {
            5,
            0,
            0,
            0});
            this.springOriginYInput.Location = new System.Drawing.Point(83, 62);
            this.springOriginYInput.Maximum = new decimal(new int[] {
            2000,
            0,
            0,
            0});
            this.springOriginYInput.Minimum = new decimal(new int[] {
            2000,
            0,
            0,
            -2147483648});
            this.springOriginYInput.Name = "springOriginYInput";
            this.springOriginYInput.Size = new System.Drawing.Size(99, 20);
            this.springOriginYInput.TabIndex = 6;
            this.springOriginYInput.ValueChanged += new System.EventHandler(this.inputField_ValueChanged);
            // 
            // lidConnectPosInput
            // 
            this.lidConnectPosInput.Increment = new decimal(new int[] {
            5,
            0,
            0,
            0});
            this.lidConnectPosInput.Location = new System.Drawing.Point(83, 108);
            this.lidConnectPosInput.Maximum = new decimal(new int[] {
            10000,
            0,
            0,
            0});
            this.lidConnectPosInput.Minimum = new decimal(new int[] {
            1000,
            0,
            0,
            -2147483648});
            this.lidConnectPosInput.Name = "lidConnectPosInput";
            this.lidConnectPosInput.Size = new System.Drawing.Size(99, 20);
            this.lidConnectPosInput.TabIndex = 7;
            this.lidConnectPosInput.ValueChanged += new System.EventHandler(this.inputField_ValueChanged);
            // 
            // springOriginXInput
            // 
            this.springOriginXInput.Increment = new decimal(new int[] {
            5,
            0,
            0,
            0});
            this.springOriginXInput.Location = new System.Drawing.Point(83, 36);
            this.springOriginXInput.Maximum = new decimal(new int[] {
            2000,
            0,
            0,
            0});
            this.springOriginXInput.Minimum = new decimal(new int[] {
            2000,
            0,
            0,
            -2147483648});
            this.springOriginXInput.Name = "springOriginXInput";
            this.springOriginXInput.Size = new System.Drawing.Size(99, 20);
            this.springOriginXInput.TabIndex = 5;
            this.springOriginXInput.ValueChanged += new System.EventHandler(this.inputField_ValueChanged);
            // 
            // endFittingRodLabel
            // 
            this.endFittingRodLabel.AutoSize = true;
            this.endFittingRodLabel.Location = new System.Drawing.Point(6, 276);
            this.endFittingRodLabel.Name = "endFittingRodLabel";
            this.endFittingRodLabel.Size = new System.Drawing.Size(69, 13);
            this.endFittingRodLabel.TabIndex = 7;
            this.endFittingRodLabel.Text = "Endfitting rod";
            // 
            // endFittingTubeLabel
            // 
            this.endFittingTubeLabel.AutoSize = true;
            this.endFittingTubeLabel.Location = new System.Drawing.Point(6, 236);
            this.endFittingTubeLabel.Name = "endFittingTubeLabel";
            this.endFittingTubeLabel.Size = new System.Drawing.Size(75, 13);
            this.endFittingTubeLabel.TabIndex = 7;
            this.endFittingTubeLabel.Text = "Endfitting tube";
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Location = new System.Drawing.Point(6, 88);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(94, 13);
            this.label8.TabIndex = 7;
            this.label8.Text = "Mount point, on lid";
            // 
            // lidConnectPosLabel
            // 
            this.lidConnectPosLabel.AutoSize = true;
            this.lidConnectPosLabel.Location = new System.Drawing.Point(6, 110);
            this.lidConnectPosLabel.Name = "lidConnectPosLabel";
            this.lidConnectPosLabel.Size = new System.Drawing.Size(47, 13);
            this.lidConnectPosLabel.TabIndex = 7;
            this.lidConnectPosLabel.Text = "Along lid";
            // 
            // label11
            // 
            this.label11.AutoSize = true;
            this.label11.Location = new System.Drawing.Point(6, 16);
            this.label11.Name = "label11";
            this.label11.Size = new System.Drawing.Size(112, 13);
            this.label11.TabIndex = 7;
            this.label11.Text = "Mount point, fixed end";
            // 
            // lidOffsetLabel
            // 
            this.lidOffsetLabel.AutoSize = true;
            this.lidOffsetLabel.Location = new System.Drawing.Point(6, 136);
            this.lidOffsetLabel.Name = "lidOffsetLabel";
            this.lidOffsetLabel.Size = new System.Drawing.Size(35, 13);
            this.lidOffsetLabel.TabIndex = 7;
            this.lidOffsetLabel.Text = "Offset";
            // 
            // springOriginXLabel
            // 
            this.springOriginXLabel.AutoSize = true;
            this.springOriginXLabel.Location = new System.Drawing.Point(6, 38);
            this.springOriginXLabel.Name = "springOriginXLabel";
            this.springOriginXLabel.Size = new System.Drawing.Size(14, 13);
            this.springOriginXLabel.TabIndex = 7;
            this.springOriginXLabel.Text = "X";
            // 
            // springOriginYLabel
            // 
            this.springOriginYLabel.AutoSize = true;
            this.springOriginYLabel.Location = new System.Drawing.Point(6, 64);
            this.springOriginYLabel.Name = "springOriginYLabel";
            this.springOriginYLabel.Size = new System.Drawing.Size(14, 13);
            this.springOriginYLabel.TabIndex = 7;
            this.springOriginYLabel.Text = "Y";
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.Location = new System.Drawing.Point(6, 200);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(41, 13);
            this.label9.TabIndex = 7;
            this.label9.Text = "Thread";
            // 
            // nbrOfSpringsLabel
            // 
            this.nbrOfSpringsLabel.AutoSize = true;
            this.nbrOfSpringsLabel.Location = new System.Drawing.Point(6, 163);
            this.nbrOfSpringsLabel.Name = "nbrOfSpringsLabel";
            this.nbrOfSpringsLabel.Size = new System.Drawing.Size(75, 13);
            this.nbrOfSpringsLabel.TabIndex = 7;
            this.nbrOfSpringsLabel.Text = "Nbr. of springs";
            // 
            // LidInputGroupBox
            // 
            this.LidInputGroupBox.Controls.Add(this.weightInput);
            this.LidInputGroupBox.Controls.Add(this.cogInput);
            this.LidInputGroupBox.Controls.Add(this.lidLengthInput);
            this.LidInputGroupBox.Controls.Add(this.startAngleInput);
            this.LidInputGroupBox.Controls.Add(this.openingAngleInput);
            this.LidInputGroupBox.Controls.Add(this.lidLengthLabel);
            this.LidInputGroupBox.Controls.Add(this.cogLabel);
            this.LidInputGroupBox.Controls.Add(this.weightLabel);
            this.LidInputGroupBox.Controls.Add(this.startAngleLabel);
            this.LidInputGroupBox.Controls.Add(this.stopAngleLabel);
            this.LidInputGroupBox.Location = new System.Drawing.Point(6, 21);
            this.LidInputGroupBox.Name = "LidInputGroupBox";
            this.LidInputGroupBox.Size = new System.Drawing.Size(188, 164);
            this.LidInputGroupBox.TabIndex = 0;
            this.LidInputGroupBox.TabStop = false;
            this.LidInputGroupBox.Text = "Lid";
            // 
            // weightInput
            // 
            this.weightInput.DecimalPlaces = 1;
            this.weightInput.Location = new System.Drawing.Point(83, 68);
            this.weightInput.Maximum = new decimal(new int[] {
            5000,
            0,
            0,
            0});
            this.weightInput.Minimum = new decimal(new int[] {
            1,
            0,
            0,
            65536});
            this.weightInput.Name = "weightInput";
            this.weightInput.RightToLeft = System.Windows.Forms.RightToLeft.No;
            this.weightInput.Size = new System.Drawing.Size(99, 20);
            this.weightInput.TabIndex = 2;
            this.weightInput.Value = new decimal(new int[] {
            1,
            0,
            0,
            65536});
            this.weightInput.ValueChanged += new System.EventHandler(this.inputField_ValueChanged);
            // 
            // cogInput
            // 
            this.cogInput.Increment = new decimal(new int[] {
            10,
            0,
            0,
            0});
            this.cogInput.Location = new System.Drawing.Point(83, 42);
            this.cogInput.Maximum = new decimal(new int[] {
            10000,
            0,
            0,
            0});
            this.cogInput.Minimum = new decimal(new int[] {
            1000,
            0,
            0,
            -2147483648});
            this.cogInput.Name = "cogInput";
            this.cogInput.Size = new System.Drawing.Size(99, 20);
            this.cogInput.TabIndex = 1;
            this.cogInput.ValueChanged += new System.EventHandler(this.inputField_ValueChanged);
            // 
            // lidLengthInput
            // 
            this.lidLengthInput.Increment = new decimal(new int[] {
            5,
            0,
            0,
            0});
            this.lidLengthInput.Location = new System.Drawing.Point(83, 16);
            this.lidLengthInput.Maximum = new decimal(new int[] {
            10000,
            0,
            0,
            0});
            this.lidLengthInput.Minimum = new decimal(new int[] {
            100,
            0,
            0,
            0});
            this.lidLengthInput.Name = "lidLengthInput";
            this.lidLengthInput.Size = new System.Drawing.Size(99, 20);
            this.lidLengthInput.TabIndex = 0;
            this.lidLengthInput.Value = new decimal(new int[] {
            100,
            0,
            0,
            0});
            this.lidLengthInput.ValueChanged += new System.EventHandler(this.inputField_ValueChanged);
            // 
            // lidLengthLabel
            // 
            this.lidLengthLabel.AutoSize = true;
            this.lidLengthLabel.Location = new System.Drawing.Point(6, 18);
            this.lidLengthLabel.Name = "lidLengthLabel";
            this.lidLengthLabel.Size = new System.Drawing.Size(53, 13);
            this.lidLengthLabel.TabIndex = 7;
            this.lidLengthLabel.Text = "Lid length";
            // 
            // cogLabel
            // 
            this.cogLabel.AutoSize = true;
            this.cogLabel.Location = new System.Drawing.Point(6, 44);
            this.cogLabel.Name = "cogLabel";
            this.cogLabel.Size = new System.Drawing.Size(35, 13);
            this.cogLabel.TabIndex = 7;
            this.cogLabel.Text = "C.o.g.";
            // 
            // weightLabel
            // 
            this.weightLabel.AutoSize = true;
            this.weightLabel.Location = new System.Drawing.Point(6, 70);
            this.weightLabel.Name = "weightLabel";
            this.weightLabel.Size = new System.Drawing.Size(41, 13);
            this.weightLabel.TabIndex = 7;
            this.weightLabel.Text = "Weight";
            // 
            // statusStripBottom
            // 
            this.statusStripBottom.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.toolStripStatusLabel1});
            this.statusStripBottom.Location = new System.Drawing.Point(0, 715);
            this.statusStripBottom.Name = "statusStripBottom";
            this.statusStripBottom.Size = new System.Drawing.Size(1173, 22);
            this.statusStripBottom.TabIndex = 23;
            this.statusStripBottom.Text = "Status";
            // 
            // toolStripStatusLabel1
            // 
            this.toolStripStatusLabel1.Name = "toolStripStatusLabel1";
            this.toolStripStatusLabel1.Size = new System.Drawing.Size(77, 17);
            this.toolStripStatusLabel1.Text = "No messages";
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.minExtLenTextBox);
            this.groupBox1.Controls.Add(this.minStrokeTextBox);
            this.groupBox1.Controls.Add(this.label1);
            this.groupBox1.Controls.Add(this.label3);
            this.groupBox1.Location = new System.Drawing.Point(3, 643);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(201, 70);
            this.groupBox1.TabIndex = 24;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Spring geometric requirements";
            // 
            // minExtLenTextBox
            // 
            this.minExtLenTextBox.Location = new System.Drawing.Point(120, 19);
            this.minExtLenTextBox.Name = "minExtLenTextBox";
            this.minExtLenTextBox.ReadOnly = true;
            this.minExtLenTextBox.Size = new System.Drawing.Size(68, 20);
            this.minExtLenTextBox.TabIndex = 20;
            // 
            // minStrokeTextBox
            // 
            this.minStrokeTextBox.Location = new System.Drawing.Point(120, 43);
            this.minStrokeTextBox.Name = "minStrokeTextBox";
            this.minStrokeTextBox.ReadOnly = true;
            this.minStrokeTextBox.Size = new System.Drawing.Size(68, 20);
            this.minStrokeTextBox.TabIndex = 20;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(12, 46);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(59, 13);
            this.label1.TabIndex = 17;
            this.label1.Text = "Min. stroke";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(12, 22);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(106, 13);
            this.label3.TabIndex = 19;
            this.label3.Text = "Min. extended length";
            // 
            // springSelectionGroupBox
            // 
            this.springSelectionGroupBox.Controls.Add(this.selectedSpringGroupBox);
            this.springSelectionGroupBox.Controls.Add(this.SpringBox);
            this.springSelectionGroupBox.Controls.Add(this.NoSpringsText);
            this.springSelectionGroupBox.Controls.Add(this.NoSpringsLabel);
            this.springSelectionGroupBox.Location = new System.Drawing.Point(211, 490);
            this.springSelectionGroupBox.Name = "springSelectionGroupBox";
            this.springSelectionGroupBox.Size = new System.Drawing.Size(400, 223);
            this.springSelectionGroupBox.TabIndex = 25;
            this.springSelectionGroupBox.TabStop = false;
            this.springSelectionGroupBox.Text = "Spring selection";
            // 
            // selectedSpringGroupBox
            // 
            this.selectedSpringGroupBox.Controls.Add(this.selectedFrictionTextBox);
            this.selectedSpringGroupBox.Controls.Add(this.selectedFrictionLabel);
            this.selectedSpringGroupBox.Controls.Add(this.selectedPartNoTextBox);
            this.selectedSpringGroupBox.Controls.Add(this.selectedPartNoLabel);
            this.selectedSpringGroupBox.Controls.Add(this.selectedForceTextBox);
            this.selectedSpringGroupBox.Controls.Add(this.selectedForceLabel);
            this.selectedSpringGroupBox.Controls.Add(this.selectedStrokeTextBox);
            this.selectedSpringGroupBox.Controls.Add(this.label10);
            this.selectedSpringGroupBox.Controls.Add(this.lengthWithEndsTextBox);
            this.selectedSpringGroupBox.Controls.Add(this.withEndsLengthLabel);
            this.selectedSpringGroupBox.Controls.Add(this.selectedLengthTextBox);
            this.selectedSpringGroupBox.Controls.Add(this.selectedLengthLabel);
            this.selectedSpringGroupBox.Controls.Add(this.selectedTypeTextBox);
            this.selectedSpringGroupBox.Controls.Add(this.selectedTypeLabel);
            this.selectedSpringGroupBox.Location = new System.Drawing.Point(219, 16);
            this.selectedSpringGroupBox.Name = "selectedSpringGroupBox";
            this.selectedSpringGroupBox.Size = new System.Drawing.Size(175, 204);
            this.selectedSpringGroupBox.TabIndex = 17;
            this.selectedSpringGroupBox.TabStop = false;
            this.selectedSpringGroupBox.Text = "Current spring";
            // 
            // selectedFrictionTextBox
            // 
            this.selectedFrictionTextBox.Location = new System.Drawing.Point(64, 177);
            this.selectedFrictionTextBox.Name = "selectedFrictionTextBox";
            this.selectedFrictionTextBox.ReadOnly = true;
            this.selectedFrictionTextBox.Size = new System.Drawing.Size(80, 20);
            this.selectedFrictionTextBox.TabIndex = 1;
            this.selectedFrictionTextBox.TabStop = false;
            // 
            // selectedFrictionLabel
            // 
            this.selectedFrictionLabel.AutoSize = true;
            this.selectedFrictionLabel.Location = new System.Drawing.Point(6, 180);
            this.selectedFrictionLabel.Name = "selectedFrictionLabel";
            this.selectedFrictionLabel.Size = new System.Drawing.Size(58, 13);
            this.selectedFrictionLabel.TabIndex = 0;
            this.selectedFrictionLabel.Text = "Friction [N]";
            // 
            // selectedPartNoTextBox
            // 
            this.selectedPartNoTextBox.Location = new System.Drawing.Point(64, 144);
            this.selectedPartNoTextBox.Name = "selectedPartNoTextBox";
            this.selectedPartNoTextBox.ReadOnly = true;
            this.selectedPartNoTextBox.Size = new System.Drawing.Size(80, 20);
            this.selectedPartNoTextBox.TabIndex = 1;
            this.selectedPartNoTextBox.TabStop = false;
            // 
            // selectedPartNoLabel
            // 
            this.selectedPartNoLabel.AutoSize = true;
            this.selectedPartNoLabel.Location = new System.Drawing.Point(6, 147);
            this.selectedPartNoLabel.Name = "selectedPartNoLabel";
            this.selectedPartNoLabel.Size = new System.Drawing.Size(44, 13);
            this.selectedPartNoLabel.TabIndex = 0;
            this.selectedPartNoLabel.Text = "Part no.";
            // 
            // selectedForceTextBox
            // 
            this.selectedForceTextBox.Location = new System.Drawing.Point(64, 118);
            this.selectedForceTextBox.Name = "selectedForceTextBox";
            this.selectedForceTextBox.ReadOnly = true;
            this.selectedForceTextBox.Size = new System.Drawing.Size(80, 20);
            this.selectedForceTextBox.TabIndex = 1;
            this.selectedForceTextBox.TabStop = false;
            // 
            // selectedForceLabel
            // 
            this.selectedForceLabel.AutoSize = true;
            this.selectedForceLabel.Location = new System.Drawing.Point(6, 121);
            this.selectedForceLabel.Name = "selectedForceLabel";
            this.selectedForceLabel.Size = new System.Drawing.Size(51, 13);
            this.selectedForceLabel.TabIndex = 0;
            this.selectedForceLabel.Text = "Force [N]";
            // 
            // selectedStrokeTextBox
            // 
            this.selectedStrokeTextBox.Location = new System.Drawing.Point(64, 92);
            this.selectedStrokeTextBox.Name = "selectedStrokeTextBox";
            this.selectedStrokeTextBox.ReadOnly = true;
            this.selectedStrokeTextBox.Size = new System.Drawing.Size(80, 20);
            this.selectedStrokeTextBox.TabIndex = 1;
            this.selectedStrokeTextBox.TabStop = false;
            // 
            // label10
            // 
            this.label10.AutoSize = true;
            this.label10.Location = new System.Drawing.Point(6, 95);
            this.label10.Name = "label10";
            this.label10.Size = new System.Drawing.Size(38, 13);
            this.label10.TabIndex = 0;
            this.label10.Text = "Stroke";
            // 
            // lengthWithEndsTextBox
            // 
            this.lengthWithEndsTextBox.Location = new System.Drawing.Point(64, 65);
            this.lengthWithEndsTextBox.Name = "lengthWithEndsTextBox";
            this.lengthWithEndsTextBox.ReadOnly = true;
            this.lengthWithEndsTextBox.Size = new System.Drawing.Size(80, 20);
            this.lengthWithEndsTextBox.TabIndex = 1;
            this.lengthWithEndsTextBox.TabStop = false;
            // 
            // withEndsLengthLabel
            // 
            this.withEndsLengthLabel.AutoSize = true;
            this.withEndsLengthLabel.Location = new System.Drawing.Point(6, 68);
            this.withEndsLengthLabel.Name = "withEndsLengthLabel";
            this.withEndsLengthLabel.Size = new System.Drawing.Size(56, 13);
            this.withEndsLengthLabel.TabIndex = 0;
            this.withEndsLengthLabel.Text = "... w. ends";
            // 
            // selectedLengthTextBox
            // 
            this.selectedLengthTextBox.Location = new System.Drawing.Point(64, 41);
            this.selectedLengthTextBox.Name = "selectedLengthTextBox";
            this.selectedLengthTextBox.ReadOnly = true;
            this.selectedLengthTextBox.Size = new System.Drawing.Size(80, 20);
            this.selectedLengthTextBox.TabIndex = 1;
            this.selectedLengthTextBox.TabStop = false;
            // 
            // selectedLengthLabel
            // 
            this.selectedLengthLabel.AutoSize = true;
            this.selectedLengthLabel.Location = new System.Drawing.Point(6, 44);
            this.selectedLengthLabel.Name = "selectedLengthLabel";
            this.selectedLengthLabel.Size = new System.Drawing.Size(40, 13);
            this.selectedLengthLabel.TabIndex = 0;
            this.selectedLengthLabel.Text = "Length";
            // 
            // selectedTypeTextBox
            // 
            this.selectedTypeTextBox.Location = new System.Drawing.Point(64, 17);
            this.selectedTypeTextBox.Name = "selectedTypeTextBox";
            this.selectedTypeTextBox.ReadOnly = true;
            this.selectedTypeTextBox.Size = new System.Drawing.Size(80, 20);
            this.selectedTypeTextBox.TabIndex = 1;
            this.selectedTypeTextBox.TabStop = false;
            // 
            // selectedTypeLabel
            // 
            this.selectedTypeLabel.AutoSize = true;
            this.selectedTypeLabel.Location = new System.Drawing.Point(6, 20);
            this.selectedTypeLabel.Name = "selectedTypeLabel";
            this.selectedTypeLabel.Size = new System.Drawing.Size(31, 13);
            this.selectedTypeLabel.TabIndex = 0;
            this.selectedTypeLabel.Text = "Type";
            // 
            // menuStrip1
            // 
            this.menuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.toolStripMenuItem1,
            this.editToolStripMenuItem});
            this.menuStrip1.Location = new System.Drawing.Point(0, 0);
            this.menuStrip1.Name = "menuStrip1";
            this.menuStrip1.Size = new System.Drawing.Size(1173, 24);
            this.menuStrip1.TabIndex = 26;
            this.menuStrip1.Text = "menuStrip1";
            // 
            // toolStripMenuItem1
            // 
            this.toolStripMenuItem1.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.restoreLastToolStripMenuItem,
            this.openToolStripMenuItem,
            this.saveToolStripMenuItem,
            this.toolStripSeparator1,
            this.printToolStripMenuItem,
            this.exitToolStripMenuItem});
            this.toolStripMenuItem1.Name = "toolStripMenuItem1";
            this.toolStripMenuItem1.Size = new System.Drawing.Size(37, 20);
            this.toolStripMenuItem1.Text = "File";
            // 
            // restoreLastToolStripMenuItem
            // 
            this.restoreLastToolStripMenuItem.Name = "restoreLastToolStripMenuItem";
            this.restoreLastToolStripMenuItem.Size = new System.Drawing.Size(174, 22);
            this.restoreLastToolStripMenuItem.Text = "Open last session...";
            this.restoreLastToolStripMenuItem.Click += new System.EventHandler(this.restoreLastToolStripMenuItem_Click);
            // 
            // openToolStripMenuItem
            // 
            this.openToolStripMenuItem.Name = "openToolStripMenuItem";
            this.openToolStripMenuItem.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.O)));
            this.openToolStripMenuItem.Size = new System.Drawing.Size(174, 22);
            this.openToolStripMenuItem.Text = "Open...";
            this.openToolStripMenuItem.Click += new System.EventHandler(this.openToolStripMenuItem_Click);
            // 
            // saveToolStripMenuItem
            // 
            this.saveToolStripMenuItem.Name = "saveToolStripMenuItem";
            this.saveToolStripMenuItem.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.S)));
            this.saveToolStripMenuItem.Size = new System.Drawing.Size(174, 22);
            this.saveToolStripMenuItem.Text = "Save...";
            this.saveToolStripMenuItem.Click += new System.EventHandler(this.saveToolStripMenuItem_Click);
            // 
            // toolStripSeparator1
            // 
            this.toolStripSeparator1.Name = "toolStripSeparator1";
            this.toolStripSeparator1.Size = new System.Drawing.Size(171, 6);
            // 
            // printToolStripMenuItem
            // 
            this.printToolStripMenuItem.Name = "printToolStripMenuItem";
            this.printToolStripMenuItem.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.P)));
            this.printToolStripMenuItem.Size = new System.Drawing.Size(174, 22);
            this.printToolStripMenuItem.Text = "Print";
            this.printToolStripMenuItem.Click += new System.EventHandler(this.printToolStripMenuItem_Click);
            // 
            // exitToolStripMenuItem
            // 
            this.exitToolStripMenuItem.Name = "exitToolStripMenuItem";
            this.exitToolStripMenuItem.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.Q)));
            this.exitToolStripMenuItem.Size = new System.Drawing.Size(174, 22);
            this.exitToolStripMenuItem.Text = "Exit";
            this.exitToolStripMenuItem.Click += new System.EventHandler(this.exitToolStripMenuItem_Click);
            // 
            // editToolStripMenuItem
            // 
            this.editToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.optionsMenuItem});
            this.editToolStripMenuItem.Name = "editToolStripMenuItem";
            this.editToolStripMenuItem.Size = new System.Drawing.Size(39, 20);
            this.editToolStripMenuItem.Text = "Edit";
            // 
            // optionsMenuItem
            // 
            this.optionsMenuItem.Name = "optionsMenuItem";
            this.optionsMenuItem.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.T)));
            this.optionsMenuItem.Size = new System.Drawing.Size(166, 22);
            this.optionsMenuItem.Text = "Options...";
            this.optionsMenuItem.Click += new System.EventHandler(this.optionsMenuItem_Click);
            // 
            // designerMailLabel
            // 
            this.designerMailLabel.AutoSize = true;
            this.designerMailLabel.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.designerMailLabel.Location = new System.Drawing.Point(7, 66);
            this.designerMailLabel.Name = "designerMailLabel";
            this.designerMailLabel.Size = new System.Drawing.Size(39, 13);
            this.designerMailLabel.TabIndex = 41;
            this.designerMailLabel.Text = "E-Mail:";
            // 
            // designerTelLabel
            // 
            this.designerTelLabel.AutoSize = true;
            this.designerTelLabel.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.designerTelLabel.Location = new System.Drawing.Point(7, 43);
            this.designerTelLabel.Name = "designerTelLabel";
            this.designerTelLabel.Size = new System.Drawing.Size(42, 13);
            this.designerTelLabel.TabIndex = 40;
            this.designerTelLabel.Text = "Tel.No:";
            // 
            // designerNameLabel
            // 
            this.designerNameLabel.AutoSize = true;
            this.designerNameLabel.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.designerNameLabel.Location = new System.Drawing.Point(7, 20);
            this.designerNameLabel.Name = "designerNameLabel";
            this.designerNameLabel.Size = new System.Drawing.Size(38, 13);
            this.designerNameLabel.TabIndex = 39;
            this.designerNameLabel.Text = "Name:";
            // 
            // customerBox
            // 
            this.customerBox.Controls.Add(this.label58);
            this.customerBox.Controls.Add(this.label57);
            this.customerBox.Controls.Add(this.label56);
            this.customerBox.Controls.Add(this.label55);
            this.customerBox.Controls.Add(this.customerMailTextBox);
            this.customerBox.Controls.Add(this.customerProjectTextBox);
            this.customerBox.Controls.Add(this.customerNameTextBox);
            this.customerBox.Controls.Add(this.customerCompanyTextBox);
            this.customerBox.Location = new System.Drawing.Point(824, 598);
            this.customerBox.Name = "customerBox";
            this.customerBox.Size = new System.Drawing.Size(344, 115);
            this.customerBox.TabIndex = 38;
            this.customerBox.TabStop = false;
            this.customerBox.Text = "Customer";
            // 
            // label58
            // 
            this.label58.AutoSize = true;
            this.label58.Location = new System.Drawing.Point(6, 90);
            this.label58.Name = "label58";
            this.label58.Size = new System.Drawing.Size(51, 13);
            this.label58.TabIndex = 9;
            this.label58.Text = "Fax/Mail:";
            // 
            // label57
            // 
            this.label57.AutoSize = true;
            this.label57.Location = new System.Drawing.Point(6, 67);
            this.label57.Name = "label57";
            this.label57.Size = new System.Drawing.Size(43, 13);
            this.label57.TabIndex = 8;
            this.label57.Text = "Project:";
            // 
            // label56
            // 
            this.label56.AutoSize = true;
            this.label56.Location = new System.Drawing.Point(6, 44);
            this.label56.Name = "label56";
            this.label56.Size = new System.Drawing.Size(38, 13);
            this.label56.TabIndex = 7;
            this.label56.Text = "Name:";
            // 
            // label55
            // 
            this.label55.AutoSize = true;
            this.label55.Location = new System.Drawing.Point(6, 21);
            this.label55.Name = "label55";
            this.label55.Size = new System.Drawing.Size(54, 13);
            this.label55.TabIndex = 6;
            this.label55.Text = "Company:";
            // 
            // customerMailTextBox
            // 
            this.customerMailTextBox.Location = new System.Drawing.Point(66, 87);
            this.customerMailTextBox.Name = "customerMailTextBox";
            this.customerMailTextBox.Size = new System.Drawing.Size(264, 20);
            this.customerMailTextBox.TabIndex = 33;
            // 
            // customerProjectTextBox
            // 
            this.customerProjectTextBox.Location = new System.Drawing.Point(66, 64);
            this.customerProjectTextBox.Name = "customerProjectTextBox";
            this.customerProjectTextBox.Size = new System.Drawing.Size(264, 20);
            this.customerProjectTextBox.TabIndex = 32;
            // 
            // customerNameTextBox
            // 
            this.customerNameTextBox.Location = new System.Drawing.Point(66, 41);
            this.customerNameTextBox.Name = "customerNameTextBox";
            this.customerNameTextBox.Size = new System.Drawing.Size(264, 20);
            this.customerNameTextBox.TabIndex = 31;
            // 
            // customerCompanyTextBox
            // 
            this.customerCompanyTextBox.Location = new System.Drawing.Point(66, 18);
            this.customerCompanyTextBox.Name = "customerCompanyTextBox";
            this.customerCompanyTextBox.Size = new System.Drawing.Size(264, 20);
            this.customerCompanyTextBox.TabIndex = 30;
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.sliderLimitLabel);
            this.groupBox2.Controls.Add(this.sliderRadioLimitOff);
            this.groupBox2.Controls.Add(this.sliderRadioLimitInput);
            this.groupBox2.Controls.Add(this.sliderRadioLimitSpring);
            this.groupBox2.Controls.Add(this.currentAngleLabel);
            this.groupBox2.Controls.Add(this.angleSlider);
            this.groupBox2.Location = new System.Drawing.Point(210, 414);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(400, 67);
            this.groupBox2.TabIndex = 45;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "Visualize motion";
            // 
            // sliderLimitLabel
            // 
            this.sliderLimitLabel.AutoSize = true;
            this.sliderLimitLabel.Location = new System.Drawing.Point(18, 47);
            this.sliderLimitLabel.Name = "sliderLimitLabel";
            this.sliderLimitLabel.Size = new System.Drawing.Size(57, 13);
            this.sliderLimitLabel.TabIndex = 22;
            this.sliderLimitLabel.Text = "Limit angle";
            // 
            // sliderRadioLimitOff
            // 
            this.sliderRadioLimitOff.AutoSize = true;
            this.sliderRadioLimitOff.Location = new System.Drawing.Point(216, 45);
            this.sliderRadioLimitOff.Name = "sliderRadioLimitOff";
            this.sliderRadioLimitOff.Size = new System.Drawing.Size(57, 17);
            this.sliderRadioLimitOff.TabIndex = 21;
            this.sliderRadioLimitOff.TabStop = true;
            this.sliderRadioLimitOff.Text = "no limit";
            this.sliderRadioLimitOff.UseVisualStyleBackColor = true;
            this.sliderRadioLimitOff.CheckedChanged += new System.EventHandler(this.radioLimitSlide);
            // 
            // sliderRadioLimitInput
            // 
            this.sliderRadioLimitInput.AutoSize = true;
            this.sliderRadioLimitInput.Location = new System.Drawing.Point(151, 45);
            this.sliderRadioLimitInput.Name = "sliderRadioLimitInput";
            this.sliderRadioLimitInput.Size = new System.Drawing.Size(60, 17);
            this.sliderRadioLimitInput.TabIndex = 21;
            this.sliderRadioLimitInput.TabStop = true;
            this.sliderRadioLimitInput.Text = "to input";
            this.sliderRadioLimitInput.UseVisualStyleBackColor = true;
            this.sliderRadioLimitInput.CheckedChanged += new System.EventHandler(this.radioLimitSlide);
            // 
            // sliderRadioLimitSpring
            // 
            this.sliderRadioLimitSpring.AutoSize = true;
            this.sliderRadioLimitSpring.Location = new System.Drawing.Point(86, 45);
            this.sliderRadioLimitSpring.Name = "sliderRadioLimitSpring";
            this.sliderRadioLimitSpring.Size = new System.Drawing.Size(65, 17);
            this.sliderRadioLimitSpring.TabIndex = 21;
            this.sliderRadioLimitSpring.TabStop = true;
            this.sliderRadioLimitSpring.Text = "to spring";
            this.sliderRadioLimitSpring.UseVisualStyleBackColor = true;
            this.sliderRadioLimitSpring.CheckedChanged += new System.EventHandler(this.radioLimitSlide);
            // 
            // chart1
            // 
            this.chart1.BorderlineColor = System.Drawing.Color.Black;
            this.chart1.BorderlineWidth = 2;
            this.chart1.BorderSkin.BackColor = System.Drawing.Color.Black;
            this.chart1.BorderSkin.BorderWidth = 2;
            this.chart1.BorderSkin.PageColor = System.Drawing.SystemColors.Control;
            chartArea1.Name = "ChartArea1";
            this.chart1.ChartAreas.Add(chartArea1);
            this.chart1.Location = new System.Drawing.Point(618, 31);
            this.chart1.Name = "chart1";
            series1.ChartArea = "ChartArea1";
            series1.ChartType = System.Windows.Forms.DataVisualization.Charting.SeriesChartType.Line;
            series1.Name = "Series1";
            this.chart1.Series.Add(series1);
            this.chart1.Size = new System.Drawing.Size(550, 380);
            this.chart1.TabIndex = 46;
            this.chart1.TabStop = false;
            this.chart1.Text = "chart1";
            title1.Name = "Title1";
            title1.Text = "Hand force [N]. Positive pulls lid.";
            this.chart1.Titles.Add(title1);
            // 
            // designerBox
            // 
            this.designerBox.Controls.Add(this.designerMailTextBox);
            this.designerBox.Controls.Add(this.designerTelTextBox);
            this.designerBox.Controls.Add(this.designerNameTextBox);
            this.designerBox.Controls.Add(this.designerTelLabel);
            this.designerBox.Controls.Add(this.designerNameLabel);
            this.designerBox.Controls.Add(this.designerMailLabel);
            this.designerBox.Location = new System.Drawing.Point(824, 499);
            this.designerBox.Name = "designerBox";
            this.designerBox.Size = new System.Drawing.Size(344, 93);
            this.designerBox.TabIndex = 47;
            this.designerBox.TabStop = false;
            this.designerBox.Text = "Designer";
            // 
            // designerMailTextBox
            // 
            this.designerMailTextBox.Location = new System.Drawing.Point(66, 63);
            this.designerMailTextBox.Name = "designerMailTextBox";
            this.designerMailTextBox.Size = new System.Drawing.Size(262, 20);
            this.designerMailTextBox.TabIndex = 42;
            // 
            // designerTelTextBox
            // 
            this.designerTelTextBox.Location = new System.Drawing.Point(66, 40);
            this.designerTelTextBox.Name = "designerTelTextBox";
            this.designerTelTextBox.Size = new System.Drawing.Size(262, 20);
            this.designerTelTextBox.TabIndex = 42;
            // 
            // designerNameTextBox
            // 
            this.designerNameTextBox.Location = new System.Drawing.Point(66, 17);
            this.designerNameTextBox.Name = "designerNameTextBox";
            this.designerNameTextBox.Size = new System.Drawing.Size(262, 20);
            this.designerNameTextBox.TabIndex = 42;
            // 
            // selfOpeningAngleLabel
            // 
            this.selfOpeningAngleLabel.AutoSize = true;
            this.selfOpeningAngleLabel.Location = new System.Drawing.Point(6, 74);
            this.selfOpeningAngleLabel.Name = "selfOpeningAngleLabel";
            this.selfOpeningAngleLabel.Size = new System.Drawing.Size(95, 13);
            this.selfOpeningAngleLabel.TabIndex = 48;
            this.selfOpeningAngleLabel.Text = "Self opening angle";
            // 
            // selfOpeningAngleTextBox
            // 
            this.selfOpeningAngleTextBox.Location = new System.Drawing.Point(107, 71);
            this.selfOpeningAngleTextBox.Name = "selfOpeningAngleTextBox";
            this.selfOpeningAngleTextBox.ReadOnly = true;
            this.selfOpeningAngleTextBox.Size = new System.Drawing.Size(87, 20);
            this.selfOpeningAngleTextBox.TabIndex = 49;
            // 
            // groupBox3
            // 
            this.groupBox3.Controls.Add(this.label4);
            this.groupBox3.Controls.Add(this.overshootTextBox);
            this.groupBox3.Controls.Add(this.maxOpeningAngleLabel);
            this.groupBox3.Controls.Add(this.maxOpeningAngleTextBox);
            this.groupBox3.Controls.Add(this.selfOpeningAngleLabel);
            this.groupBox3.Controls.Add(this.selfOpeningAngleTextBox);
            this.groupBox3.Location = new System.Drawing.Point(618, 499);
            this.groupBox3.Name = "groupBox3";
            this.groupBox3.Size = new System.Drawing.Size(200, 100);
            this.groupBox3.TabIndex = 52;
            this.groupBox3.TabStop = false;
            this.groupBox3.Text = "Lid angle summary";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(6, 47);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(59, 13);
            this.label4.TabIndex = 52;
            this.label4.Text = "Over-shoot";
            // 
            // overshootTextBox
            // 
            this.overshootTextBox.Location = new System.Drawing.Point(107, 44);
            this.overshootTextBox.Name = "overshootTextBox";
            this.overshootTextBox.ReadOnly = true;
            this.overshootTextBox.Size = new System.Drawing.Size(87, 20);
            this.overshootTextBox.TabIndex = 53;
            // 
            // maxOpeningAngleLabel
            // 
            this.maxOpeningAngleLabel.AutoSize = true;
            this.maxOpeningAngleLabel.Location = new System.Drawing.Point(6, 20);
            this.maxOpeningAngleLabel.Name = "maxOpeningAngleLabel";
            this.maxOpeningAngleLabel.Size = new System.Drawing.Size(97, 13);
            this.maxOpeningAngleLabel.TabIndex = 50;
            this.maxOpeningAngleLabel.Text = "Max opening angle";
            // 
            // maxOpeningAngleTextBox
            // 
            this.maxOpeningAngleTextBox.Location = new System.Drawing.Point(107, 17);
            this.maxOpeningAngleTextBox.Name = "maxOpeningAngleTextBox";
            this.maxOpeningAngleTextBox.ReadOnly = true;
            this.maxOpeningAngleTextBox.Size = new System.Drawing.Size(87, 20);
            this.maxOpeningAngleTextBox.TabIndex = 51;
            // 
            // endsBox
            // 
            this.endsBox.Controls.Add(this.endFittings2Label);
            this.endsBox.Controls.Add(this.endFittings1Label);
            this.endsBox.Location = new System.Drawing.Point(618, 627);
            this.endsBox.Name = "endsBox";
            this.endsBox.Size = new System.Drawing.Size(200, 86);
            this.endsBox.TabIndex = 53;
            this.endsBox.TabStop = false;
            this.endsBox.Text = "End fittings";
            // 
            // endFittings2Label
            // 
            this.endFittings2Label.AutoSize = true;
            this.endFittings2Label.Location = new System.Drawing.Point(9, 50);
            this.endFittings2Label.Name = "endFittings2Label";
            this.endFittings2Label.Size = new System.Drawing.Size(44, 13);
            this.endFittings2Label.TabIndex = 1;
            this.endFittings2Label.Text = "Welded";
            // 
            // endFittings1Label
            // 
            this.endFittings1Label.AutoSize = true;
            this.endFittings1Label.Location = new System.Drawing.Point(9, 25);
            this.endFittings1Label.Name = "endFittings1Label";
            this.endFittings1Label.Size = new System.Drawing.Size(44, 13);
            this.endFittings1Label.TabIndex = 0;
            this.endFittings1Label.Text = "Welded";
            // 
            // SpringForms
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.Control;
            this.ClientSize = new System.Drawing.Size(1173, 737);
            this.Controls.Add(this.endsBox);
            this.Controls.Add(this.groupBox3);
            this.Controls.Add(this.designerBox);
            this.Controls.Add(this.chart1);
            this.Controls.Add(this.groupBox2);
            this.Controls.Add(this.customerBox);
            this.Controls.Add(this.springSelectionGroupBox);
            this.Controls.Add(this.groupBox1);
            this.Controls.Add(this.statusStripBottom);
            this.Controls.Add(this.menuStrip1);
            this.Controls.Add(this.GeometricInputGroup);
            this.Controls.Add(this.hatchBox);
            this.MainMenuStrip = this.menuStrip1;
            this.Name = "SpringForms";
            this.Text = "Form1";
            ((System.ComponentModel.ISupportInitialize)(this.hatchBox)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.openingAngleInput)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.startAngleInput)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.angleSlider)).EndInit();
            this.GeometricInputGroup.ResumeLayout(false);
            this.temperatureGroupBox.ResumeLayout(false);
            this.temperatureGroupBox.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.temperatureInput)).EndInit();
            this.SpringInputGroupBox.ResumeLayout(false);
            this.SpringInputGroupBox.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.nbrOfSpringsInput)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.lidOffsetInput)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.springOriginYInput)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.lidConnectPosInput)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.springOriginXInput)).EndInit();
            this.LidInputGroupBox.ResumeLayout(false);
            this.LidInputGroupBox.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.weightInput)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.cogInput)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.lidLengthInput)).EndInit();
            this.statusStripBottom.ResumeLayout(false);
            this.statusStripBottom.PerformLayout();
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.springSelectionGroupBox.ResumeLayout(false);
            this.springSelectionGroupBox.PerformLayout();
            this.selectedSpringGroupBox.ResumeLayout(false);
            this.selectedSpringGroupBox.PerformLayout();
            this.menuStrip1.ResumeLayout(false);
            this.menuStrip1.PerformLayout();
            this.customerBox.ResumeLayout(false);
            this.customerBox.PerformLayout();
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.chart1)).EndInit();
            this.designerBox.ResumeLayout(false);
            this.designerBox.PerformLayout();
            this.groupBox3.ResumeLayout(false);
            this.groupBox3.PerformLayout();
            this.endsBox.ResumeLayout(false);
            this.endsBox.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.PictureBox hatchBox;
        private System.Windows.Forms.Button inputSubmit;
        private System.Windows.Forms.ListBox SpringBox;
        private System.Windows.Forms.Label startAngleLabel;
        public  System.Windows.Forms.NumericUpDown openingAngleInput;
        public  System.Windows.Forms.NumericUpDown startAngleInput;
        private System.Windows.Forms.TrackBar angleSlider;
        private System.Windows.Forms.Label stopAngleLabel;
        private System.Windows.Forms.Label currentAngleLabel;
        private System.Windows.Forms.Label NoSpringsText;
        private System.Windows.Forms.Label NoSpringsLabel;
        private System.Windows.Forms.ComboBox endFittingTubeBox;
        private System.Windows.Forms.GroupBox GeometricInputGroup;
        private System.Windows.Forms.GroupBox LidInputGroupBox;
        public  System.Windows.Forms.NumericUpDown weightInput;
        public  System.Windows.Forms.NumericUpDown cogInput;
        public  System.Windows.Forms.NumericUpDown lidLengthInput;
        private System.Windows.Forms.Label lidLengthLabel;
        private System.Windows.Forms.Label cogLabel;
        private System.Windows.Forms.Label weightLabel;
        private System.Windows.Forms.GroupBox SpringInputGroupBox;
        public  System.Windows.Forms.NumericUpDown nbrOfSpringsInput;
        public  System.Windows.Forms.NumericUpDown springOriginYInput;
        public  System.Windows.Forms.NumericUpDown springOriginXInput;
        private System.Windows.Forms.Label springOriginXLabel;
        private System.Windows.Forms.Label springOriginYLabel;
        private System.Windows.Forms.Label nbrOfSpringsLabel;
        private System.Windows.Forms.Label label11;
        public  System.Windows.Forms.NumericUpDown lidOffsetInput;
        public  System.Windows.Forms.NumericUpDown lidConnectPosInput;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.Label lidConnectPosLabel;
        private System.Windows.Forms.Label lidOffsetLabel;
        private System.Windows.Forms.RadioButton threadRadioAll;
        private System.Windows.Forms.ComboBox endFittingRodBox;
        private System.Windows.Forms.RadioButton threadRadioM8;
        private System.Windows.Forms.RadioButton threadRadioM6;
        private System.Windows.Forms.Label endFittingRodLabel;
        private System.Windows.Forms.Label endFittingTubeLabel;
        private System.Windows.Forms.Label label9;
        private System.Windows.Forms.Button ResetButton;
        private System.Windows.Forms.StatusStrip statusStripBottom;
        private System.Windows.Forms.GroupBox groupBox1;
        public  System.Windows.Forms.TextBox minExtLenTextBox;
        public  System.Windows.Forms.TextBox minStrokeTextBox;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.GroupBox springSelectionGroupBox;
        private System.Windows.Forms.GroupBox selectedSpringGroupBox;
        public  System.Windows.Forms.TextBox selectedPartNoTextBox;
        private System.Windows.Forms.Label selectedPartNoLabel;
        public  System.Windows.Forms.TextBox selectedForceTextBox;
        private System.Windows.Forms.Label selectedForceLabel;
        public  System.Windows.Forms.TextBox selectedStrokeTextBox;
        private System.Windows.Forms.Label label10;
        public  System.Windows.Forms.TextBox selectedLengthTextBox;
        private System.Windows.Forms.Label selectedLengthLabel;
        public  System.Windows.Forms.TextBox selectedTypeTextBox;
        private System.Windows.Forms.Label selectedTypeLabel;
        public  System.Windows.Forms.TextBox lengthWithEndsTextBox;
        private System.Windows.Forms.Label withEndsLengthLabel;
        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.ToolStripMenuItem toolStripMenuItem1;
        private System.Windows.Forms.ToolStripMenuItem editToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem optionsMenuItem;
        private System.Windows.Forms.Label designerMailLabel;
        private System.Windows.Forms.Label designerTelLabel;
        private System.Windows.Forms.Label designerNameLabel;
        private System.Windows.Forms.GroupBox customerBox;
        private System.Windows.Forms.Label label58;
        private System.Windows.Forms.Label label57;
        private System.Windows.Forms.Label label56;
        private System.Windows.Forms.Label label55;
        public  System.Windows.Forms.TextBox customerMailTextBox;
        public  System.Windows.Forms.TextBox customerProjectTextBox;
        public  System.Windows.Forms.TextBox customerNameTextBox;
        public  System.Windows.Forms.TextBox customerCompanyTextBox;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.RadioButton sliderRadioLimitOff;
        private System.Windows.Forms.RadioButton sliderRadioLimitInput;
        private System.Windows.Forms.RadioButton sliderRadioLimitSpring;
        private System.Windows.Forms.Label sliderLimitLabel;
        private System.Windows.Forms.DataVisualization.Charting.Chart chart1;
        private System.Windows.Forms.ToolStripMenuItem openToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem saveToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem printToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem exitToolStripMenuItem;
        private System.Windows.Forms.ToolStripSeparator toolStripSeparator1;
        private System.Windows.Forms.ToolStripMenuItem restoreLastToolStripMenuItem;
        public  System.Windows.Forms.TextBox selectedFrictionTextBox;
        private System.Windows.Forms.Label selectedFrictionLabel;
        private System.Windows.Forms.GroupBox designerBox;
        public  System.Windows.Forms.TextBox designerMailTextBox;
        public  System.Windows.Forms.TextBox designerTelTextBox;
        public  System.Windows.Forms.TextBox designerNameTextBox;
        private System.Windows.Forms.GroupBox temperatureGroupBox;
        public  System.Windows.Forms.NumericUpDown temperatureInput;
        private System.Windows.Forms.Label temperatureLabel;
        private System.Windows.Forms.ToolStripStatusLabel toolStripStatusLabel1;
        private System.Windows.Forms.Label selfOpeningAngleLabel;
        public System.Windows.Forms.TextBox selfOpeningAngleTextBox;
        private System.Windows.Forms.ToolTip toolTip1;
        private System.Windows.Forms.RadioButton threadRadioWeld;
        private System.Windows.Forms.GroupBox groupBox3;
        private System.Windows.Forms.Label maxOpeningAngleLabel;
        public System.Windows.Forms.TextBox maxOpeningAngleTextBox;
        private System.Windows.Forms.Label label4;
        public System.Windows.Forms.TextBox overshootTextBox;
        private System.Windows.Forms.GroupBox endsBox;
        private System.Windows.Forms.Label endFittings2Label;
        private System.Windows.Forms.Label endFittings1Label;
    }
}

