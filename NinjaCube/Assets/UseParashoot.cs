using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class UseParashoot : MonoBehaviour
{
    public Transform player;
    public Rigidbody rb;
    public float parashootEffectiveness;
    bool spaceClicked = false;
    bool meshOn = false;
    public float turningRate;

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKey("space") && player.position.y > 2)
        {
            spaceClicked = true;
            //player.eulerAngles = new Vector3(0, 0, 0);
            rb.angularVelocity = new Vector3(0, 0, 0);
            if (player.rotation != Quaternion.Euler(new Vector3(0, 0, 0)))
            {
                Quaternion q = Quaternion.RotateTowards(player.rotation, Quaternion.Euler(new Vector3(0, 0, 0)), turningRate * Time.deltaTime);
                //if (Mathf.Abs(q[0] + q[1] + q[2]) < Mathf.Abs(-(q[0]) + -(q[1]) + -(q[2]))) 
                //{
                //    player.rotation = q;
                //} else
                //{
                //    player.rotation = Quaternion.Euler(new Vector3(-(q[0]), -(q[1]), -(q[2])));
                //}
                player.rotation = q;
            }
            else
            {
                rb.angularVelocity = new Vector3(0, 0, 0);
            }
            if (!meshOn)
            {
                gameObject.GetComponent<MeshRenderer>().enabled = true;
                meshOn = true;
            }
        }
        else
        {
            spaceClicked = false;
        }
        if (!spaceClicked)
        {
            meshOn = false;
            gameObject.GetComponent<MeshRenderer>().enabled = false;
        }
        else
        {
            spaceClicked = false;
            

        }
  
    }

    void FixedUpdate()
    {
        if (spaceClicked)
        {
            rb.AddForce(0, parashootEffectiveness, 0);
        }
    }
}
