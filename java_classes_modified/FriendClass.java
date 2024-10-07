@Entity
@Table(name="friend")
public class Friend implements Serializable {

    @Id
    @Column(name="userId")
    private long userId;

    @Column(name="isRepost")
    private boolean isRepost;

    @Column(name="dateCreated")
    private Date dateCreated;

}

