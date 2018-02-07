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
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Drawing;
using System.Windows.Forms;
using PdfSharp;
using PdfSharp.Drawing;
using PdfSharp.Pdf;
using PdfSharp.Pdf.IO;


namespace HatchTest
{
    internal class PdfManager
    {
        SpringForms myParent = null;
        XFont font9 = new XFont("Verdana", 9);
        XFont font10 = new XFont("Verdana", 10);
        XFont font10b = new XFont("Verdana", 10, XFontStyle.Bold);
        XFont font9i = new XFont("Verdana", 9, XFontStyle.Italic);
        string picturesPath_, logoFile;
        XImage imageLogo;
        Rectangle pageBorder = new Rectangle(35, 115, 520, 655);
        Pen penBlack = new Pen(Brushes.Black, 1);
        Pen penGray = new Pen(Brushes.Gray, 1);

        public PdfManager(SpringForms parent)
        {
            picturesPath_ = "Pictures";
            logoFile = Path.Combine(picturesPath_,"logotype.png");
            imageLogo = XImage.FromFile(logoFile);

            this.myParent = parent;
            string test1 = myParent.nbrOfSpringsInput.Value.ToString();
        }

        public bool makePDF(string fileName)
        {
            // Create a new PDF document
            PdfDocument document = new PdfDocument();

            string documentFileName = Path.Combine(myParent.tempPath,fileName);

            // First Page
            PdfPage page1 = document.AddPage();
            XGraphics pdf1 = XGraphics.FromPdfPage(page1);

            makeHeader(pdf1, logoFile);

            addHatchGraph(pdf1);

            addGeometricInfo(pdf1);

            addProjectInfo(pdf1);

            makeFooter(pdf1);

            pdf1.Dispose();

            // Second Page
            PdfPage page2 = document.AddPage();
            XGraphics pdf2 = XGraphics.FromPdfPage(page2);

            makeHeader(pdf2, logoFile, "2");

            addForceGraph(pdf2);

            makeSpringImage(pdf2);

            pdf2.DrawRectangle(penBlack, 35, 115, 520, 655);

            pdf2.DrawLine(penBlack, 35, 512, 555, 512);

            makeProposal(pdf2);

            makeComments(pdf2);

            makeFooter(pdf2);

            try
            {
                document.Save(documentFileName);
                System.Diagnostics.Process.Start(documentFileName);
            }
            catch
            {
                myParent.warning("Failed to open PDF file: " + documentFileName);
                myParent.notify("Please close open PDF in order to generate a new.");
            }

            pdf2.Dispose();

            return true;
        }

        private void addHatchGraph(XGraphics pdf1)
        {
            XImage imageLid = myParent.hatchBitmap;
            pdf1.DrawImage(imageLid, 106, 145, 380, 380);
            pdf1.DrawRectangle(penGray, 106, 145, 380, 380);
        }

        private void addGeometricInfo(XGraphics pdf1)
        {
            // Collect data. Preferrably from the hatch itself?
            string lidLength = ((int)myParent.currentHatch.lid.length).ToString();
            string lidWeight = ((int)myParent.currentHatch.lid.mass).ToString();
            string lidCog = ((int)myParent.currentHatch.lid.cog().length()).ToString();
            string startAngle = myParent.startAngleInput.Value.ToString();
            string openingAngle = myParent.openingAngleInput.Value.ToString();
            string maxOpeningAngle = myParent.getOpeningDeg2Deg(myParent.currentHatch.maxSpringDeg).ToString();
            string lidConnect = myParent.lidConnectPosInput.Value.ToString();
            string lidOffset = myParent.lidOffsetInput.Value.ToString();
            string springFixX = myParent.springOriginXInput.Value.ToString();
            string springFixY = myParent.springOriginYInput.Value.ToString();

            // Gemoteric Info.
            pdf1.DrawString("Geometric Info", font10b, XBrushes.Black, 45, 620);

            pdf1.DrawString("Lid length: " + lidLength + " mm", font9, XBrushes.Black, 45, 635);

            pdf1.DrawString("Lid weight: " + lidWeight + " kg", font9, XBrushes.Black, 45, 650);

            pdf1.DrawString("Opening angle:", font9, XBrushes.Black, 45, 665);
            pdf1.DrawString("Desired: " + openingAngle + "º", font9, XBrushes.Black, 171, 665);
            pdf1.DrawString("Actual: " + maxOpeningAngle + "º", font9, XBrushes.Black, 171, 680);

            pdf1.DrawString("Mounting Point, Fixed:", font9, XBrushes.Black, 45, 700);
            pdf1.DrawString("X: " + springFixX + " mm", font9, XBrushes.Black, 171, 700);
            pdf1.DrawString("Y: " + springFixY + " mm", font9, XBrushes.Black, 171, 715);

            pdf1.DrawString("Mounting Point, Lid:", font9, XBrushes.Black, 45, 735);
            pdf1.DrawString("From Hinge: " + lidConnect + " mm", font9, XBrushes.Black, 171, 735);
            pdf1.DrawString("Offset: " + lidOffset + " mm", font9, XBrushes.Black, 171, 750);
        }

        private void addProjectInfo(XGraphics pdf1)
        {
            pdf1.DrawString("Customer Info", font10b, XBrushes.Black, 310, 620);

            pdf1.DrawString("Company:", font9, XBrushes.Black, 310, 635);
            pdf1.DrawString(myParent.customerCompanyTextBox.Text, font9, XBrushes.Black, 371, 635);

            pdf1.DrawString("Name:", font9, XBrushes.Black, 310, 650);
            pdf1.DrawString(myParent.customerNameTextBox.Text, font9, XBrushes.Black, 371, 650);

            pdf1.DrawString("Project:", font9, XBrushes.Black, 310, 665);
            pdf1.DrawString(myParent.customerProjectTextBox.Text, font9, XBrushes.Black, 371, 665);

            pdf1.DrawString("Fax/Mail:", font9, XBrushes.Black, 310, 680);
            pdf1.DrawString(myParent.customerMailTextBox.Text, font9, XBrushes.Black, 371, 680);

            // Designer Info.
            pdf1.DrawString("Designer Info", font10b, XBrushes.Black, 310, 700);

            pdf1.DrawString("Designed By:", font9, XBrushes.Black, 310, 715);
            pdf1.DrawString(myParent.designerNameTextBox.Text, font9, XBrushes.Black, 385, 715);

            pdf1.DrawString("Tel. No:", font9, XBrushes.Black, 310, 730);
            pdf1.DrawString(myParent.designerTelTextBox.Text, font9, XBrushes.Black, 385, 730);

            pdf1.DrawString("Mail: " + myParent.designerMailTextBox.Text, font9, XBrushes.Black, 310, 745);

            // Drawing of the vertical line between "Geometric Info" and "Customer Info".
            pdf1.DrawLine(penGray, 300, 605, 300, 770);


        }

        private void addForceGraph(XGraphics pdf2)
        {
            // Get the graph image and put it on the PDF
            XImage ximg = XImage.FromGdiPlusImage(myParent.chartImage);
            pdf2.DrawImage(ximg, 106, 145, 380, 270);
            pdf2.DrawRectangle(penGray, 105, 144, 381, 271);

        }

        private void makeHeader(XGraphics pdf, string logoFile, string pageNum="1")
        {
            pdf.DrawImage(imageLogo, 168, 35, 250, 66);
            pdf.DrawRectangle(penBlack, pageBorder);
            
            string customerProject = myParent.customerProjectTextBox.Text;
            pdf.DrawString(customerProject + " / Page "+pageNum+" of 2", font9, XBrushes.Black, 35, 112);
            pdf.DrawLine(penBlack, 35, 605, 555, 605);
        }

        private void makeFooter(XGraphics pdf)
        {
            string company = myParent.optionsForm.getFooterByName("companyTextBox");
            string postAddress = myParent.optionsForm.getFooterByName("streetTextBox");
            string zip = myParent.optionsForm.getFooterByName("zipTextBox");
            string region = myParent.optionsForm.getFooterByName("regionTextBox");
            string telNat = myParent.optionsForm.getFooterByName("pageFooterTelNational");
            string telInt = myParent.optionsForm.getFooterByName("pageFooterTelInternational");
            string faxNat = myParent.optionsForm.getFooterByName("pageFooterFaxNational");
            string faxInt = myParent.optionsForm.getFooterByName("pageFooterFaxInternational");


            // Contact Information.
            pdf.DrawString("Postal Address", font9i, XBrushes.Black, 35, 780);
            pdf.DrawString(company, font9, XBrushes.Black, 35, 790);
            pdf.DrawString(postAddress, font9, XBrushes.Black, 35, 800);
            pdf.DrawString(zip + " " + region, font9, XBrushes.Black, 35, 810);

            pdf.DrawString("Telephone", font9i, XBrushes.Black, 239, 780);
            pdf.DrawString("Nat. " + telNat, font9, XBrushes.Black, 239, 800);
            pdf.DrawString("Int. " + telInt, font9, XBrushes.Black, 239, 810);
            pdf.DrawString("Telefax", font9i, XBrushes.Black, 403, 780);
            pdf.DrawString("Nat. " + faxNat, font9, XBrushes.Black, 403, 800);
            pdf.DrawString("Int. " + faxInt, font9, XBrushes.Black, 403, 810);
        }

        private void makeSpringImage(XGraphics pdf)
        {
            Hatch hatch = myParent.currentHatch;
            if (hatch.spring.isWelded())
            {
                addPicture(pdf, "gasspring_weld.jpg", 115, 424);
                string weldedPic = picPath("gasspring_weld.jpg");
                pdf.DrawImage(Image.FromFile(weldedPic), 115, 424);
            }
            else
            {
                string fileNameRod = hatch.spring.endFittings[1].partNumber+"R.png";
                string fileNameTube = hatch.spring.endFittings[0].partNumber+"T.png";
                addPicture(pdf, "gasspring.jpg", 155,424);
                addPicture(pdf, fileNameRod, 50, 424);
                addPicture(pdf, fileNameTube, 470, 424);
            }
        }

        private void makeProposal(XGraphics pdf)
        {
            Spring spring = myParent.currentHatch.spring;
            pdf.DrawString("Proposal", font10b, XBrushes.Black, 45, 527);
            pdf.DrawString("Product key:", font9, XBrushes.Black, 45, 542);
            pdf.DrawString(spring.name, font9i, XBrushes.Black, 160, 542);
            pdf.DrawString("Part number:", font9, XBrushes.Black, 350, 542);
            pdf.DrawString(spring.partNumber, font9i, XBrushes.Black, 420, 542);

            pdf.DrawString("Number of springs:", font9, XBrushes.Black, 45, 557);
            pdf.DrawString(myParent.currentHatch.nSprings.ToString(), font9i, XBrushes.Black, 160, 557);

            string efitTube2 = myParent.optionsForm.getCommentByName("endfitFixTextBox1");
            string efitRod2 = myParent.optionsForm.getCommentByName("endfitFixTextBox2");

            pdf.DrawString("Endfitting, Tube:", font9, XBrushes.Black, 45, 572);
            pdf.DrawString(spring.endFittings[0].name+" "+spring.endFittings[0].partNumber, font9i, XBrushes.Black, 160, 572);
            pdf.DrawString("Endfitting 2, Tube:", font9, XBrushes.Black, 350, 572);
            pdf.DrawString(efitTube2, font9i, XBrushes.Black, 460, 572);

            pdf.DrawString("Endfitting, Rod:", font9, XBrushes.Black, 45, 587);
            pdf.DrawString(spring.endFittings[1].name + " " + spring.endFittings[1].partNumber, font9i, XBrushes.Black, 160, 587);
            pdf.DrawString("Endfitting 2, Rod:", font9, XBrushes.Black, 350, 587);
            pdf.DrawString(efitRod2, font9i, XBrushes.Black, 460, 587);

            //pdf.DrawLine(penBlack, 35, 600, 555, 600);
        }

        private void makeComments(XGraphics pdf)
        {
            for (int i = 0; i < 7; i++)
            {
                pdf.DrawString("Comments", font10b, XBrushes.Black, 45, 615);
                string name = "userFreeText" + i.ToString();
                string comment = myParent.optionsForm.getCommentByName(name);
                pdf.DrawString(comment, font9, XBrushes.Black, 45, 630 + i * 15);
            }
        }

        private string picPath(string fileName)
        {
            return Path.Combine(picturesPath_, fileName);
        }

        private void addPicture(XGraphics pdf, string name, int x, int y)
        {
            string img = picPath(name);
            try
            {
                pdf.DrawImage(Image.FromFile(img), x, y);
            }
            catch
            {
                myParent.warning("Error in PDF when loading picture: "+img);
                pdf.DrawString("Missing image", font10b, XBrushes.Gray, x+10,y+10);
            }
        }
    }
}
