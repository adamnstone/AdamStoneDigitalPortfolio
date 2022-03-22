using UnityEngine;

public class ChangeDetectionMode : MonoBehaviour
{
    public Rigidbody rb;
    public PlayerMovement player;
    public float changeSpeed = 175f;
    void Update()
    {
        if (player.forwardsForce >= changeSpeed && rb.collisionDetectionMode != CollisionDetectionMode.Continuous) 
        {
            rb.collisionDetectionMode = CollisionDetectionMode.Continuous;
        }
    }
}
