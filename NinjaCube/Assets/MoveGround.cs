using UnityEngine;

public class MoveGround : MonoBehaviour
{
    public Transform ground;
    public Transform player;
    public float groundOffsetFromPlayerZ;
    public float groundResetDistance;
    float currentMolduo = 0;
    void Update()
    {
        checkMolduo();
    }

    void checkMolduo()
    {
        if (Mathf.Floor(player.position.z / groundResetDistance) > currentMolduo)
        {
            currentMolduo = Mathf.Floor(player.position.z / groundResetDistance);
            ground.position = new Vector3(0, 0, player.position.z-groundOffsetFromPlayerZ+2000/2);
        }
    }
}
