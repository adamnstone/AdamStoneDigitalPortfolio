using UnityEngine;
using UnityEngine.UI;
using System.Collections;
using System.IO.Ports;
using System.Threading;

public class Manager : MonoBehaviour
{
    private SerialPort port = new SerialPort("COM4", 9600);

    public Slider[] sliders;

    public void MoveMotors()
    {
        string x = ((int)sliders[0].value).ToString();
        string y = ((int)sliders[1].value).ToString();
        string z = ((int)sliders[2].value).ToString();
        Send(Pad(x, 3) + Pad(y, 3) + Pad(z, 3));
    }
    
    void Send(string message)
    {
        port.Open();
        port.Write(message);
    }

    string Pad(string s, int amount)
    {
        string toReturn = string.Empty;
        for (int i = 0; i < amount - s.Length; i++)
        {
            toReturn += " ";
        }
        toReturn += s;
        return toReturn;
    }
}
