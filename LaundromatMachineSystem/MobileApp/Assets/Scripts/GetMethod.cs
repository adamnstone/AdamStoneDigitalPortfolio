using System.Collections;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;

public class GetMethod : MonoBehaviour
{
    InputField outputArea;
    public Dropdown duration;
    public Text IPInput;

    void Awake()
    {
        outputArea = GameObject.Find("OutputArea").GetComponent<InputField>();
        GameObject.Find("GetButton").GetComponent<Button>().onClick.AddListener(GetData);
    }

    void GetData() => StartCoroutine(GetData_Coroutine());

    char GetNum(char c)
    {
        if (c == 'a')
        {
            return '1';
        }
        else if (c == 'e')
        {
            return '3';
        }
        else if (c == 'i')
        {
            return '9';
        }
        else if (c == 'q')
        {
            return '4';
        }
        else if (c == 'x')
        {
            return '5';
        }
        else if (c == 'd')
        {
            return '2';
        }
        else if (c == 's')
        {
            return '6';
        }
        else if (c == 'y')
        {
            return '7';
        }
        else if (c == 'u')
        {
            return '8';
        }
        else if (c == 'p')
        {
            return '0';
        }
        else if (c == 'v')
        {
            return '.';
        }
        return ' ';
    }

    string ConvertToIP(string qr)
    {
        string final = "";
        foreach (char c in qr)
        {
            final += GetNum(c);
        }
        return final;
    }

    string ScanQR()
    {
        return "aidvasuvusvdqq";
    }

    IEnumerator GetData_Coroutine()
    {
        //if (duration.text.)
        string qr = ScanQR();
        string ip = ConvertToIP(qr);
        ip = "192.168.86.244";
        ip = IPInput.text;
        Debug.Log(ip);
        outputArea.text = "Loading...";
        Debug.Log("http://" + ip + "?code=0xfbce434ee3&duration=" + duration.options[duration.value].text);
        string uri = "http://" + ip + "?code=0xfbce434ee3&duration=" + duration.options[duration.value].text;
        using (UnityWebRequest request = UnityWebRequest.Get(uri))
        {
            yield return request.SendWebRequest();
            if (request.isNetworkError || request.isHttpError)
                outputArea.text = request.error;
            else
                outputArea.text = request.downloadHandler.text;
        }
    }
}