using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    public Rigidbody rb;
    public Transform t;
    public float sidewaysForce;
    public float forwardsForce;
    public CollideEnemy collideEnemyScript;

    bool left = false;
    bool right = false;

    // Update is called once per frame
    void Update()
    {
        if (t.position.y <= 0)
        {
            collideEnemyScript.EndGame();
        }
        if (Input.GetKey("left"))
        {
            left = true;
        }
        if (Input.GetKey("right"))
        {
            right = true;
        }

    }

    void FixedUpdate()
    {
        if (left)
        {
            rb.AddForce(-sidewaysForce * Time.fixedDeltaTime, 0, 0, ForceMode.VelocityChange);
            left = false;
        }
        if (right)
        {
            rb.AddForce(sidewaysForce * Time.fixedDeltaTime, 0, 0, ForceMode.VelocityChange);
            right = false;
        }
        rb.AddForce(0, 0, forwardsForce * Time.fixedDeltaTime, ForceMode.VelocityChange);
    }
}
