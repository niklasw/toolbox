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


﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace HatchTest
{
    public partial class OptionsForm : Form
    {
        SpringForms myParent = null;

        List<TextBox> customTextBoxes_;
        List<TextBox> pageFooterTextBoxes_;

        public OptionsForm(SpringForms parent)
        {
            this.myParent = parent;
            InitializeComponent();

            customTextBoxes_ = new List<TextBox>();
            customTextBoxes_.Add(endfitFixTextBox1);
            customTextBoxes_.Add(endfitFixTextBox2);

            customTextBoxes_.Add(userFreeTextBox1);
            customTextBoxes_.Add(userFreeTextBox2);
            customTextBoxes_.Add(userFreeTextBox3);
            customTextBoxes_.Add(userFreeTextBox4);
            customTextBoxes_.Add(userFreeTextBox5);
            customTextBoxes_.Add(userFreeTextBox6);
            customTextBoxes_.Add(userFreeTextBox7);

            pageFooterTextBoxes_ = new List<TextBox>();
            pageFooterTextBoxes_.Add(companyTextBox);
            pageFooterTextBoxes_.Add(streetTextBox);
            pageFooterTextBoxes_.Add(zipTextBox);
            pageFooterTextBoxes_.Add(regionTextBox);
            pageFooterTextBoxes_.Add(pageFooterTelNational);
            pageFooterTextBoxes_.Add(pageFooterTelInternational);
            pageFooterTextBoxes_.Add(pageFooterFaxNational);
            pageFooterTextBoxes_.Add(pageFooterFaxInternational);
        }

        private void optionsCancelButton_Click(object sender, EventArgs e)
        {
            Form.ActiveForm.Close();
        }

        private void optionsOKbutton_Click(object sender, EventArgs e)
        {
            Form.ActiveForm.Close();
        }
        private void optionsClearButton_Click(object sender, EventArgs e)
        {
            foreach(TextBox box in customTextBoxes_)
            {
                box.Text = "";
            }

        }

        private void fillTextBoxFromList
        (
            TextBox box,
            List<TextBox> L
        )
        {
            foreach (TextBox b in L)
            {
                if (b.Name == box.Name)
                {
                    box.Text = b.Text;
                    break;
                }
            }

        }

        public List<TextBox> customTextBoxes
        {
            get { return customTextBoxes_; }
        }

        public List<TextBox> pageFooterTextBoxes
        {
            get { return pageFooterTextBoxes_; }
        }

        public string getCommentByName(string name)
        {
            string ret = "--";
            foreach( TextBox b in customTextBoxes_)
            {
                if (b.Name == name)
                {
                    ret = b.Text;
                    break;
                }
            }
            return ret;
        }
        public string getFooterByName(string name)
        {
            string ret = "--";
            foreach (TextBox b in pageFooterTextBoxes_)
            {
                if (b.Name == name)
                {
                    ret = b.Text;
                    break;
                }
            }
            return ret;
        }
    }
}
