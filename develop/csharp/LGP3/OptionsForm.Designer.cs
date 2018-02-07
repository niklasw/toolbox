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


﻿namespace HatchTest
{
    public partial class OptionsForm
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
            this.optionsTabControl = new System.Windows.Forms.TabControl();
            this.optionsTabPageFoot = new System.Windows.Forms.TabPage();
            this.groupBox5 = new System.Windows.Forms.GroupBox();
            this.label10 = new System.Windows.Forms.Label();
            this.pageFooterFaxInternational = new System.Windows.Forms.TextBox();
            this.label11 = new System.Windows.Forms.Label();
            this.pageFooterFaxNational = new System.Windows.Forms.TextBox();
            this.groupBox4 = new System.Windows.Forms.GroupBox();
            this.label9 = new System.Windows.Forms.Label();
            this.pageFooterTelNational = new System.Windows.Forms.TextBox();
            this.pageFooterTelInternational = new System.Windows.Forms.TextBox();
            this.label8 = new System.Windows.Forms.Label();
            this.label20 = new System.Windows.Forms.Label();
            this.postalAddressGroupBox = new System.Windows.Forms.GroupBox();
            this.regionTextBox = new System.Windows.Forms.TextBox();
            this.regionLabel = new System.Windows.Forms.Label();
            this.zipTextBox = new System.Windows.Forms.TextBox();
            this.zipLabel = new System.Windows.Forms.Label();
            this.streetTextBox = new System.Windows.Forms.TextBox();
            this.streetLabel = new System.Windows.Forms.Label();
            this.companyTextBox = new System.Windows.Forms.TextBox();
            this.companyLabel = new System.Windows.Forms.Label();
            this.optionsTabPrintComments = new System.Windows.Forms.TabPage();
            this.optionsClearButton = new System.Windows.Forms.Button();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.userFreeTextBox7 = new System.Windows.Forms.TextBox();
            this.userFreeTextBox6 = new System.Windows.Forms.TextBox();
            this.userFreeTextBox5 = new System.Windows.Forms.TextBox();
            this.userFreeTextBox4 = new System.Windows.Forms.TextBox();
            this.userFreeTextBox3 = new System.Windows.Forms.TextBox();
            this.userFreeTextBox2 = new System.Windows.Forms.TextBox();
            this.userFreeTextBox1 = new System.Windows.Forms.TextBox();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.label2 = new System.Windows.Forms.Label();
            this.endfitFixTextBox2 = new System.Windows.Forms.TextBox();
            this.endfitFixTextBox1 = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.optionsCancelButton = new System.Windows.Forms.Button();
            this.optionsOKbutton = new System.Windows.Forms.Button();
            this.optionsTabControl.SuspendLayout();
            this.optionsTabPageFoot.SuspendLayout();
            this.groupBox5.SuspendLayout();
            this.groupBox4.SuspendLayout();
            this.postalAddressGroupBox.SuspendLayout();
            this.optionsTabPrintComments.SuspendLayout();
            this.groupBox2.SuspendLayout();
            this.groupBox1.SuspendLayout();
            this.SuspendLayout();
            // 
            // optionsTabControl
            // 
            this.optionsTabControl.Controls.Add(this.optionsTabPageFoot);
            this.optionsTabControl.Controls.Add(this.optionsTabPrintComments);
            this.optionsTabControl.Location = new System.Drawing.Point(-2, -1);
            this.optionsTabControl.Name = "optionsTabControl";
            this.optionsTabControl.SelectedIndex = 0;
            this.optionsTabControl.Size = new System.Drawing.Size(517, 429);
            this.optionsTabControl.TabIndex = 0;
            // 
            // optionsTabPageFoot
            // 
            this.optionsTabPageFoot.Controls.Add(this.groupBox5);
            this.optionsTabPageFoot.Controls.Add(this.groupBox4);
            this.optionsTabPageFoot.Controls.Add(this.label20);
            this.optionsTabPageFoot.Controls.Add(this.postalAddressGroupBox);
            this.optionsTabPageFoot.Location = new System.Drawing.Point(4, 22);
            this.optionsTabPageFoot.Name = "optionsTabPageFoot";
            this.optionsTabPageFoot.Padding = new System.Windows.Forms.Padding(3);
            this.optionsTabPageFoot.Size = new System.Drawing.Size(509, 403);
            this.optionsTabPageFoot.TabIndex = 0;
            this.optionsTabPageFoot.Text = "Page footer";
            this.optionsTabPageFoot.UseVisualStyleBackColor = true;
            // 
            // groupBox5
            // 
            this.groupBox5.Controls.Add(this.label10);
            this.groupBox5.Controls.Add(this.pageFooterFaxInternational);
            this.groupBox5.Controls.Add(this.label11);
            this.groupBox5.Controls.Add(this.pageFooterFaxNational);
            this.groupBox5.Location = new System.Drawing.Point(27, 266);
            this.groupBox5.Name = "groupBox5";
            this.groupBox5.Size = new System.Drawing.Size(397, 66);
            this.groupBox5.TabIndex = 43;
            this.groupBox5.TabStop = false;
            this.groupBox5.Text = "Telefax";
            // 
            // label10
            // 
            this.label10.AutoSize = true;
            this.label10.Location = new System.Drawing.Point(6, 16);
            this.label10.Name = "label10";
            this.label10.Size = new System.Drawing.Size(49, 13);
            this.label10.TabIndex = 28;
            this.label10.Text = "National:";
            // 
            // pageFooterFaxInternational
            // 
            this.pageFooterFaxInternational.Location = new System.Drawing.Point(123, 36);
            this.pageFooterFaxInternational.Name = "pageFooterFaxInternational";
            this.pageFooterFaxInternational.Size = new System.Drawing.Size(268, 20);
            this.pageFooterFaxInternational.TabIndex = 8;
            // 
            // label11
            // 
            this.label11.AutoSize = true;
            this.label11.Location = new System.Drawing.Point(6, 39);
            this.label11.Name = "label11";
            this.label11.Size = new System.Drawing.Size(68, 13);
            this.label11.TabIndex = 33;
            this.label11.Text = "International:";
            // 
            // pageFooterFaxNational
            // 
            this.pageFooterFaxNational.Location = new System.Drawing.Point(123, 13);
            this.pageFooterFaxNational.Name = "pageFooterFaxNational";
            this.pageFooterFaxNational.Size = new System.Drawing.Size(268, 20);
            this.pageFooterFaxNational.TabIndex = 7;
            // 
            // groupBox4
            // 
            this.groupBox4.Controls.Add(this.label9);
            this.groupBox4.Controls.Add(this.pageFooterTelNational);
            this.groupBox4.Controls.Add(this.pageFooterTelInternational);
            this.groupBox4.Controls.Add(this.label8);
            this.groupBox4.Location = new System.Drawing.Point(27, 189);
            this.groupBox4.Name = "groupBox4";
            this.groupBox4.Size = new System.Drawing.Size(397, 71);
            this.groupBox4.TabIndex = 42;
            this.groupBox4.TabStop = false;
            this.groupBox4.Text = "Telephone";
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.Location = new System.Drawing.Point(6, 18);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(49, 13);
            this.label9.TabIndex = 29;
            this.label9.Text = "National:";
            // 
            // pageFooterTelNational
            // 
            this.pageFooterTelNational.Location = new System.Drawing.Point(123, 15);
            this.pageFooterTelNational.Name = "pageFooterTelNational";
            this.pageFooterTelNational.Size = new System.Drawing.Size(268, 20);
            this.pageFooterTelNational.TabIndex = 5;
            // 
            // pageFooterTelInternational
            // 
            this.pageFooterTelInternational.Location = new System.Drawing.Point(123, 41);
            this.pageFooterTelInternational.Name = "pageFooterTelInternational";
            this.pageFooterTelInternational.Size = new System.Drawing.Size(268, 20);
            this.pageFooterTelInternational.TabIndex = 6;
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Location = new System.Drawing.Point(6, 41);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(68, 13);
            this.label8.TabIndex = 34;
            this.label8.Text = "International:";
            // 
            // label20
            // 
            this.label20.AutoSize = true;
            this.label20.Location = new System.Drawing.Point(24, 349);
            this.label20.Name = "label20";
            this.label20.Size = new System.Drawing.Size(332, 13);
            this.label20.TabIndex = 41;
            this.label20.Text = "This information is specific to the user. It will not be saved to projects.";
            // 
            // postalAddressGroupBox
            // 
            this.postalAddressGroupBox.Controls.Add(this.regionTextBox);
            this.postalAddressGroupBox.Controls.Add(this.regionLabel);
            this.postalAddressGroupBox.Controls.Add(this.zipTextBox);
            this.postalAddressGroupBox.Controls.Add(this.zipLabel);
            this.postalAddressGroupBox.Controls.Add(this.streetTextBox);
            this.postalAddressGroupBox.Controls.Add(this.streetLabel);
            this.postalAddressGroupBox.Controls.Add(this.companyTextBox);
            this.postalAddressGroupBox.Controls.Add(this.companyLabel);
            this.postalAddressGroupBox.Location = new System.Drawing.Point(27, 38);
            this.postalAddressGroupBox.Name = "postalAddressGroupBox";
            this.postalAddressGroupBox.Size = new System.Drawing.Size(397, 145);
            this.postalAddressGroupBox.TabIndex = 0;
            this.postalAddressGroupBox.TabStop = false;
            this.postalAddressGroupBox.Text = "Postal address";
            // 
            // regionTextBox
            // 
            this.regionTextBox.Location = new System.Drawing.Point(104, 108);
            this.regionTextBox.Name = "regionTextBox";
            this.regionTextBox.Size = new System.Drawing.Size(287, 20);
            this.regionTextBox.TabIndex = 4;
            // 
            // regionLabel
            // 
            this.regionLabel.AutoSize = true;
            this.regionLabel.Location = new System.Drawing.Point(6, 111);
            this.regionLabel.Name = "regionLabel";
            this.regionLabel.Size = new System.Drawing.Size(29, 13);
            this.regionLabel.TabIndex = 0;
            this.regionLabel.Text = "Area";
            // 
            // zipTextBox
            // 
            this.zipTextBox.Location = new System.Drawing.Point(104, 82);
            this.zipTextBox.Name = "zipTextBox";
            this.zipTextBox.Size = new System.Drawing.Size(287, 20);
            this.zipTextBox.TabIndex = 3;
            // 
            // zipLabel
            // 
            this.zipLabel.AutoSize = true;
            this.zipLabel.Location = new System.Drawing.Point(6, 85);
            this.zipLabel.Name = "zipLabel";
            this.zipLabel.Size = new System.Drawing.Size(51, 13);
            this.zipLabel.TabIndex = 0;
            this.zipLabel.Text = "ZIP code";
            // 
            // streetTextBox
            // 
            this.streetTextBox.Location = new System.Drawing.Point(104, 56);
            this.streetTextBox.Name = "streetTextBox";
            this.streetTextBox.Size = new System.Drawing.Size(287, 20);
            this.streetTextBox.TabIndex = 2;
            // 
            // streetLabel
            // 
            this.streetLabel.AutoSize = true;
            this.streetLabel.Location = new System.Drawing.Point(6, 59);
            this.streetLabel.Name = "streetLabel";
            this.streetLabel.Size = new System.Drawing.Size(35, 13);
            this.streetLabel.TabIndex = 0;
            this.streetLabel.Text = "Street";
            // 
            // companyTextBox
            // 
            this.companyTextBox.Location = new System.Drawing.Point(104, 30);
            this.companyTextBox.Name = "companyTextBox";
            this.companyTextBox.Size = new System.Drawing.Size(287, 20);
            this.companyTextBox.TabIndex = 1;
            // 
            // companyLabel
            // 
            this.companyLabel.AutoSize = true;
            this.companyLabel.Location = new System.Drawing.Point(6, 33);
            this.companyLabel.Name = "companyLabel";
            this.companyLabel.Size = new System.Drawing.Size(51, 13);
            this.companyLabel.TabIndex = 0;
            this.companyLabel.Text = "Company";
            // 
            // optionsTabPrintComments
            // 
            this.optionsTabPrintComments.Controls.Add(this.optionsClearButton);
            this.optionsTabPrintComments.Controls.Add(this.groupBox2);
            this.optionsTabPrintComments.Controls.Add(this.groupBox1);
            this.optionsTabPrintComments.Controls.Add(this.label3);
            this.optionsTabPrintComments.Location = new System.Drawing.Point(4, 22);
            this.optionsTabPrintComments.Name = "optionsTabPrintComments";
            this.optionsTabPrintComments.Padding = new System.Windows.Forms.Padding(3);
            this.optionsTabPrintComments.Size = new System.Drawing.Size(509, 403);
            this.optionsTabPrintComments.TabIndex = 1;
            this.optionsTabPrintComments.Text = "Print comments";
            this.optionsTabPrintComments.UseVisualStyleBackColor = true;
            // 
            // optionsClearButton
            // 
            this.optionsClearButton.Location = new System.Drawing.Point(32, 374);
            this.optionsClearButton.Name = "optionsClearButton";
            this.optionsClearButton.Size = new System.Drawing.Size(75, 23);
            this.optionsClearButton.TabIndex = 46;
            this.optionsClearButton.Text = "Clear";
            this.optionsClearButton.UseVisualStyleBackColor = true;
            this.optionsClearButton.Click += new System.EventHandler(this.optionsClearButton_Click);
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.userFreeTextBox7);
            this.groupBox2.Controls.Add(this.userFreeTextBox6);
            this.groupBox2.Controls.Add(this.userFreeTextBox5);
            this.groupBox2.Controls.Add(this.userFreeTextBox4);
            this.groupBox2.Controls.Add(this.userFreeTextBox3);
            this.groupBox2.Controls.Add(this.userFreeTextBox2);
            this.groupBox2.Controls.Add(this.userFreeTextBox1);
            this.groupBox2.Location = new System.Drawing.Point(32, 181);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(444, 185);
            this.groupBox2.TabIndex = 9;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "Comments For Customer";
            // 
            // userFreeTextBox7
            // 
            this.userFreeTextBox7.Location = new System.Drawing.Point(7, 158);
            this.userFreeTextBox7.MaxLength = 70;
            this.userFreeTextBox7.Name = "userFreeTextBox7";
            this.userFreeTextBox7.Size = new System.Drawing.Size(431, 20);
            this.userFreeTextBox7.TabIndex = 6;
            // 
            // userFreeTextBox6
            // 
            this.userFreeTextBox6.Location = new System.Drawing.Point(7, 135);
            this.userFreeTextBox6.MaxLength = 70;
            this.userFreeTextBox6.Name = "userFreeTextBox6";
            this.userFreeTextBox6.Size = new System.Drawing.Size(431, 20);
            this.userFreeTextBox6.TabIndex = 5;
            // 
            // userFreeTextBox5
            // 
            this.userFreeTextBox5.Location = new System.Drawing.Point(7, 112);
            this.userFreeTextBox5.MaxLength = 70;
            this.userFreeTextBox5.Name = "userFreeTextBox5";
            this.userFreeTextBox5.Size = new System.Drawing.Size(431, 20);
            this.userFreeTextBox5.TabIndex = 4;
            // 
            // userFreeTextBox4
            // 
            this.userFreeTextBox4.Location = new System.Drawing.Point(7, 89);
            this.userFreeTextBox4.MaxLength = 70;
            this.userFreeTextBox4.Name = "userFreeTextBox4";
            this.userFreeTextBox4.Size = new System.Drawing.Size(431, 20);
            this.userFreeTextBox4.TabIndex = 3;
            // 
            // userFreeTextBox3
            // 
            this.userFreeTextBox3.Location = new System.Drawing.Point(7, 66);
            this.userFreeTextBox3.MaxLength = 70;
            this.userFreeTextBox3.Name = "userFreeTextBox3";
            this.userFreeTextBox3.Size = new System.Drawing.Size(431, 20);
            this.userFreeTextBox3.TabIndex = 2;
            // 
            // userFreeTextBox2
            // 
            this.userFreeTextBox2.Location = new System.Drawing.Point(7, 44);
            this.userFreeTextBox2.MaxLength = 70;
            this.userFreeTextBox2.Name = "userFreeTextBox2";
            this.userFreeTextBox2.Size = new System.Drawing.Size(431, 20);
            this.userFreeTextBox2.TabIndex = 1;
            // 
            // userFreeTextBox1
            // 
            this.userFreeTextBox1.Location = new System.Drawing.Point(7, 21);
            this.userFreeTextBox1.MaxLength = 70;
            this.userFreeTextBox1.Name = "userFreeTextBox1";
            this.userFreeTextBox1.Size = new System.Drawing.Size(431, 20);
            this.userFreeTextBox1.TabIndex = 0;
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.label2);
            this.groupBox1.Controls.Add(this.endfitFixTextBox2);
            this.groupBox1.Controls.Add(this.endfitFixTextBox1);
            this.groupBox1.Controls.Add(this.label1);
            this.groupBox1.Location = new System.Drawing.Point(32, 51);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(235, 117);
            this.groupBox1.TabIndex = 7;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Endfittings";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(4, 70);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(72, 13);
            this.label2.TabIndex = 3;
            this.label2.Text = "Endfit 2, Rod:";
            // 
            // endfitFixTextBox2
            // 
            this.endfitFixTextBox2.Location = new System.Drawing.Point(7, 86);
            this.endfitFixTextBox2.MaxLength = 27;
            this.endfitFixTextBox2.Name = "endfitFixTextBox2";
            this.endfitFixTextBox2.Size = new System.Drawing.Size(151, 20);
            this.endfitFixTextBox2.TabIndex = 2;
            // 
            // endfitFixTextBox1
            // 
            this.endfitFixTextBox1.Location = new System.Drawing.Point(7, 37);
            this.endfitFixTextBox1.MaxLength = 27;
            this.endfitFixTextBox1.Name = "endfitFixTextBox1";
            this.endfitFixTextBox1.Size = new System.Drawing.Size(151, 20);
            this.endfitFixTextBox1.TabIndex = 1;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(7, 20);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(77, 13);
            this.label1.TabIndex = 0;
            this.label1.Text = "Endfit 2, Tube:";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(29, 35);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(324, 13);
            this.label3.TabIndex = 8;
            this.label3.Text = "Here you can write what other endfittings that are going to be used.";
            // 
            // optionsCancelButton
            // 
            this.optionsCancelButton.Location = new System.Drawing.Point(433, 434);
            this.optionsCancelButton.Name = "optionsCancelButton";
            this.optionsCancelButton.Size = new System.Drawing.Size(75, 23);
            this.optionsCancelButton.TabIndex = 21;
            this.optionsCancelButton.Text = "Cancel";
            this.optionsCancelButton.UseVisualStyleBackColor = true;
            this.optionsCancelButton.Click += new System.EventHandler(this.optionsCancelButton_Click);
            // 
            // optionsOKbutton
            // 
            this.optionsOKbutton.Location = new System.Drawing.Point(352, 434);
            this.optionsOKbutton.Name = "optionsOKbutton";
            this.optionsOKbutton.Size = new System.Drawing.Size(75, 23);
            this.optionsOKbutton.TabIndex = 20;
            this.optionsOKbutton.Text = "OK";
            this.optionsOKbutton.UseVisualStyleBackColor = true;
            this.optionsOKbutton.Click += new System.EventHandler(this.optionsOKbutton_Click);
            // 
            // OptionsForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(517, 463);
            this.Controls.Add(this.optionsCancelButton);
            this.Controls.Add(this.optionsOKbutton);
            this.Controls.Add(this.optionsTabControl);
            this.Name = "OptionsForm";
            this.Text = "Options";
            this.optionsTabControl.ResumeLayout(false);
            this.optionsTabPageFoot.ResumeLayout(false);
            this.optionsTabPageFoot.PerformLayout();
            this.groupBox5.ResumeLayout(false);
            this.groupBox5.PerformLayout();
            this.groupBox4.ResumeLayout(false);
            this.groupBox4.PerformLayout();
            this.postalAddressGroupBox.ResumeLayout(false);
            this.postalAddressGroupBox.PerformLayout();
            this.optionsTabPrintComments.ResumeLayout(false);
            this.optionsTabPrintComments.PerformLayout();
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.TabControl optionsTabControl;
        private System.Windows.Forms.TabPage optionsTabPageFoot;
        private System.Windows.Forms.TabPage optionsTabPrintComments;
        private System.Windows.Forms.GroupBox postalAddressGroupBox;
        private System.Windows.Forms.TextBox regionTextBox;
        private System.Windows.Forms.Label regionLabel;
        private System.Windows.Forms.TextBox zipTextBox;
        private System.Windows.Forms.Label zipLabel;
        private System.Windows.Forms.TextBox streetTextBox;
        private System.Windows.Forms.Label streetLabel;
        private System.Windows.Forms.TextBox companyTextBox;
        private System.Windows.Forms.Label companyLabel;
        private System.Windows.Forms.GroupBox groupBox5;
        private System.Windows.Forms.Label label10;
        private System.Windows.Forms.TextBox pageFooterFaxInternational;
        private System.Windows.Forms.Label label11;
        private System.Windows.Forms.TextBox pageFooterFaxNational;
        private System.Windows.Forms.GroupBox groupBox4;
        private System.Windows.Forms.Label label9;
        private System.Windows.Forms.TextBox pageFooterTelNational;
        private System.Windows.Forms.TextBox pageFooterTelInternational;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.Label label20;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.TextBox userFreeTextBox7;
        private System.Windows.Forms.TextBox userFreeTextBox6;
        private System.Windows.Forms.TextBox userFreeTextBox5;
        private System.Windows.Forms.TextBox userFreeTextBox4;
        private System.Windows.Forms.TextBox userFreeTextBox3;
        private System.Windows.Forms.TextBox userFreeTextBox2;
        private System.Windows.Forms.TextBox userFreeTextBox1;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox endfitFixTextBox2;
        private System.Windows.Forms.TextBox endfitFixTextBox1;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Button optionsCancelButton;
        private System.Windows.Forms.Button optionsOKbutton;
        private System.Windows.Forms.Button optionsClearButton;
    }
}
