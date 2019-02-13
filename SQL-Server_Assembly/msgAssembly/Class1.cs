using System;
using System.Text;
using Microsoft.SqlServer.Server;
using System.Data.SqlClient;


public partial class RealTimeLogs
    {
      /*  [Microsoft.SqlServer.Server.SqlProcedure]
        public static void MySQLCLR()
        {
            SqlContext.Pipe.Send("This text is from the sample SQLCLR procedure MySQLCLR\n");
        }*/
    [SqlTrigger(Name = @"RealTimeLogs", Target = "[dbo].[t_report_result]", Event = "FOR INSERT")]
    public static void RTLogs()
    {
        SqlCommand command=null;
        SqlDataReader reader=null;
        SqlTriggerContext triggContext = SqlContext.TriggerContext;
      
        switch (triggContext.TriggerAction)
        {
            case TriggerAction.Insert:
                pushToSlack(command, reader, "Insert","AlgoExecLogs");
                break;
            default:
                break;
        }
    }


/*
 * Push Notifications to Slack
 */
    public static void pushToSlack(SqlCommand command,SqlDataReader reader,string action, string type)
    {
       
        string postdata = null;
        using (SqlConnection connection = new SqlConnection(@"context connection=true"))
        {

            connection.Open();
            command = new SqlCommand(@"SELECT * FROM INSERTED;", connection);   
            reader = command.ExecuteReader();
            reader.Read();


            postdata = "*Realtime Algorithm Reporting* \n" + " Algorithm ID : "
            + (string)reader[1].ToString() +
            "\n Test Case Status : "
            + (string)reader[4].ToString() +
             "\n Test Case Details : "
            + (string)reader[5].ToString()
            + "\n Execution Time : "
            + (string)reader[6].ToString();


            string webhookUrl = "https://hooks.slack.com/services/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";
            Message message = new Message(webhookUrl, postdata, "#realtime_logs", ":beetle:", "QA-LOG", true);
            message.Send();
            reader.Close();

        }
    }
}